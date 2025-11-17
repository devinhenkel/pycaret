"""
Main Application Module

Creates and configures the Gradio interface for the PyCaret ML Workflow Manager.
"""

import gradio as gr
import pandas as pd
from typing import Tuple, Optional, Dict, Any
from src.modules.state_manager import StateManager
from src.modules.data_handler import DataHandler
from src.modules.config_manager import ConfigManager
from src.modules.pycaret_wrapper import PyCaretWrapper
from src.modules.visualization import VisualizationManager
from src.modules.model_manager import ModelManager
from src.utils.constants import (
    WORKFLOW_STEPS, 
    PROBLEM_TYPES, 
    PROBLEM_TYPE_LABELS,
    PROBLEM_TYPE_DESCRIPTIONS
)


def handle_file_upload(
    file: Optional[gr.File],
    state: StateManager,
    data_handler: DataHandler
) -> Tuple[str, pd.DataFrame, Dict[str, Any], str]:
    """
    Handle file upload, validation, and preview generation.
    
    Returns:
        Tuple of (status_message, preview_dataframe, statistics_dict, error_message)
    """
    if file is None:
        return "Please upload a file.", None, None, ""
    
    try:
        # Load file
        df, error = data_handler.load_file(file.name)
        if error:
            return f"❌ Error: {error}", None, None, ""
        
        # Validate data
        is_valid, validation_msg = data_handler.validate_data(df)
        if not is_valid:
            return f"❌ Validation Error: {validation_msg}", None, None, ""
        
        # Store in state
        stats = data_handler.get_data_statistics(df)
        state.set_data(df, stats)
        
        # Generate preview (first 10 rows)
        preview = df.head(10)
        
        # Format status message
        status = f"✅ File loaded successfully!\n"
        status += f"📊 Dataset: {len(df)} rows × {len(df.columns)} columns\n"
        if validation_msg:
            status += f"⚠️ {validation_msg}\n"
        
        return status, preview, stats, ""
        
    except Exception as e:
        return f"❌ Error processing file: {str(e)}", None, None, ""


def handle_problem_type_selection(
    problem_type: Optional[str],
    state: StateManager,
    data_handler: DataHandler
) -> Tuple[str, list]:
    """
    Handle problem type selection and update target column dropdown.
    
    Returns:
        Tuple of (description_text, target_column_choices)
    """
    if problem_type is None:
        return "", []
    
    # Store problem type
    state.set_problem_type(problem_type)
    
    # Get description
    description = f"**{PROBLEM_TYPE_LABELS[problem_type]}**\n\n"
    description += PROBLEM_TYPE_DESCRIPTIONS[problem_type]
    
    # Get target column choices
    df = state.get_data()
    target_choices = []
    
    if df is not None:
        target_choices = list(df.columns)
        
        # Auto-detect target column
        if problem_type in ['classification', 'regression']:
            detected = data_handler.detect_target_column(df, problem_type)
            if detected:
                description += f"\n\n💡 Suggested target column: **{detected}**"
    
    return description, target_choices


def handle_target_column_selection(
    target_column: Optional[str],
    state: StateManager
) -> str:
    """Handle target column selection."""
    if target_column:
        state.set_target_column(target_column)
        return f"✅ Target column selected: **{target_column}**"
    return ""


def handle_setup_configuration(
    session_id: str,
    train_size: float,
    cv_folds: int,
    state: StateManager,
    config_manager: ConfigManager
) -> Tuple[Dict[str, Any], str]:
    """
    Build and validate setup configuration.
    
    Returns:
        Tuple of (setup_summary_dict, status_message)
    """
    problem_type = state.get_problem_type()
    target_column = state.get_target_column()
    
    if problem_type is None:
        return {}, "❌ Please select a problem type first (Step 2)."
    
    if problem_type in ['classification', 'regression'] and not target_column:
        return {}, "❌ Please select a target column first (Step 2)."
    
    # Build configuration
    config = config_manager.build_setup_config(
        problem_type=problem_type,
        target_column=target_column,
        session_id=session_id if session_id else None,
        train_size=train_size,
        fold=int(cv_folds) if problem_type in ['classification', 'regression', 'time_series'] else None,
    )
    
    # Validate configuration
    is_valid, error_msg = config_manager.validate_config(config, problem_type)
    if not is_valid:
        return {}, f"❌ Configuration Error: {error_msg}"
    
    # Store configuration
    state.set_setup_config(config)
    
    # Generate summary
    summary = config_manager.get_setup_summary(config, problem_type)
    
    return summary, "✅ Configuration ready. Click 'Initialize Setup' to proceed."


def handle_setup_initialization(
    state: StateManager,
    pycaret_wrapper: PyCaretWrapper,
    viz_manager: VisualizationManager
) -> str:
    """
    Initialize PyCaret setup.
    
    Returns:
        Status message
    """
    problem_type = state.get_problem_type()
    config = state.get_setup_config()
    data = state.get_data()
    
    if problem_type is None or config is None or data is None:
        return "❌ Missing required information. Please complete Steps 1-3."
    
    try:
        # Initialize PyCaret setup
        setup, error = pycaret_wrapper.initialize_setup(
            problem_type=problem_type,
            data=data,
            config=config
        )
        
        if error:
            return f"❌ Setup Error: {error}"
        
        # Store setup
        state.set_pycaret_setup(setup)
        viz_manager.set_problem_type(problem_type)
        viz_manager.set_setup(setup)
        
        return "✅ PyCaret setup initialized successfully! You can now compare models in Step 4."
        
    except Exception as e:
        return f"❌ Error initializing setup: {str(e)}"


def handle_model_comparison(
    state: StateManager,
    pycaret_wrapper: PyCaretWrapper
) -> Tuple[pd.DataFrame, str, list]:
    """
    Compare all available models.
    
    Returns:
        Tuple of (results_dataframe, status_message, model_choices_list)
    """
    setup = state.get_pycaret_setup()
    
    if setup is None:
        return None, "❌ Please initialize setup first (Step 3).", []
    
    try:
        # Update wrapper setup
        pycaret_wrapper.setup = setup
        pycaret_wrapper.problem_type = state.get_problem_type()
        
        # Compare models
        results, error = pycaret_wrapper.compare_models()
        
        if error:
            return None, f"❌ Comparison Error: {error}", []
        
        # Store results
        state.set_compare_results(results)
        
        # Extract model names for selection
        if isinstance(results, pd.DataFrame):
            model_choices = list(results.index) if hasattr(results, 'index') else []
        else:
            # If results is a single model, wrap it
            model_choices = [str(results)]
        
        status = f"✅ Model comparison complete! Found {len(model_choices)} models."
        return results, status, model_choices
        
    except Exception as e:
        return None, f"❌ Error comparing models: {str(e)}", []


def handle_model_evaluation(
    model_name: str,
    state: StateManager,
    pycaret_wrapper: PyCaretWrapper,
    viz_manager: VisualizationManager
) -> Tuple[Dict[str, Any], list, str]:
    """
    Evaluate a selected model.
    
    Returns:
        Tuple of (metrics_dict, plot_choices_list, status_message)
    """
    if not model_name:
        return {}, [], ""
    
    try:
        # Get or create model
        model = state.get_trained_model(model_name)
        
        if model is None:
            # Create model if not already trained
            model, error = pycaret_wrapper.get_model(model_name)
            if error:
                return {}, [], f"❌ Error: {error}"
            
            # Store model
            state.add_trained_model(model_name, model)
        
        # Set current model
        state.set_current_model(model_name)
        
        # Get available plots
        problem_type = state.get_problem_type()
        plot_choices = viz_manager.get_available_plots(problem_type)
        
        # Get metrics (placeholder - would need to pull from PyCaret)
        metrics = {"status": "Model loaded successfully"}
        
        return metrics, plot_choices, f"✅ Model {model_name} loaded for evaluation."
        
    except Exception as e:
        return {}, [], f"❌ Error: {str(e)}"


def handle_plot_generation(
    plot_type: str,
    state: StateManager,
    viz_manager: VisualizationManager
) -> Tuple[Any, str]:
    """
    Generate a plot for the current model.
    
    Returns:
        Tuple of (plot_object, status_message)
    """
    if not plot_type:
        return None, ""
    
    model_name = state.get_current_model()
    if not model_name:
        return None, "❌ Please select a model first."
    
    try:
        model = state.get_trained_model(model_name)
        if model is None:
            return None, "❌ Model not found."
        
        plot, error = viz_manager.generate_plot(model, plot_type)
        
        if error:
            return None, f"❌ Plot Error: {error}"
        
        return plot, f"✅ Generated {plot_type} plot."
        
    except Exception as e:
        return None, f"❌ Error generating plot: {str(e)}"


def handle_model_export(
    model_name: str,
    state: StateManager,
    model_manager: ModelManager
) -> Tuple[Dict[str, Any], str, str]:
    """
    Prepare model for export.
    
    Returns:
        Tuple of (summary_dict, model_file_path, metadata_file_path)
    """
    if not model_name:
        return {}, None, None
    
    try:
        model = state.get_trained_model(model_name)
        if model is None:
            return {}, None, None
        
        problem_type = state.get_problem_type()
        config = state.get_setup_config()
        metrics = state.get_model_metrics(model_name) or {}
        
        # Generate metadata
        metadata = model_manager.generate_metadata(
            model_name=model_name,
            problem_type=problem_type,
            setup_config=config or {},
            metrics=metrics
        )
        
        # Save model
        model_path, error = model_manager.save_model(
            model=model,
            problem_type=problem_type,
            model_name=model_name
        )
        
        if error:
            return metadata, None, None
        
        # Save metadata
        metadata_path, error2 = model_manager.save_metadata(metadata)
        
        return metadata, model_path, metadata_path
        
    except Exception as e:
        return {}, None, None


def create_app():
    """
    Create and configure the Gradio application.
    
    Returns:
        Gradio Blocks interface
    """
    # Initialize managers (these will be shared across all event handlers)
    # Note: In a real Gradio app, we'd use gr.State() for these
    # For now, we'll create them here and pass them through closures
    data_handler = DataHandler()
    config_manager = ConfigManager()
    pycaret_wrapper = PyCaretWrapper()
    viz_manager = VisualizationManager()
    model_manager = ModelManager()
    
    # Create Gradio Blocks interface
    with gr.Blocks(title="PyCaret ML Workflow Manager", theme=gr.themes.Soft()) as app:
        gr.Markdown("# PyCaret ML Workflow Manager")
        gr.Markdown("Complete machine learning workflow from data upload to model export.")
        
        # State component - stores session state
        state_component = gr.State(value=StateManager())
        
        # Create tabs for workflow steps
        with gr.Tabs() as tabs:
            # Step 1: Upload Data
            with gr.Tab("Step 1: Upload Data"):
                gr.Markdown("### Upload Your Dataset")
                file_upload = gr.File(
                    label="Upload Dataset",
                    file_types=[".csv", ".xlsx", ".xls", ".parquet"],
                )
                upload_status = gr.Markdown("")
                data_preview = gr.Dataframe(label="Data Preview")
                data_stats = gr.JSON(label="Dataset Statistics")
            
            # Step 2: Select Problem Type
            with gr.Tab("Step 2: Select Problem Type"):
                gr.Markdown("### Choose Your ML Problem Type")
                problem_type = gr.Radio(
                    choices=PROBLEM_TYPES,
                    label="Problem Type",
                    value=None,
                )
                problem_description = gr.Markdown("")
                target_column = gr.Dropdown(
                    choices=[],
                    label="Target Column (if applicable)",
                    interactive=True,
                )
            
            # Step 3: Configure Setup
            with gr.Tab("Step 3: Configure Setup"):
                gr.Markdown("### Configure PyCaret Setup")
                with gr.Row():
                    session_id = gr.Textbox(
                        label="Session ID (optional)",
                        placeholder="Leave empty for auto-generated",
                    )
                    train_size = gr.Slider(
                        minimum=0.1,
                        maximum=0.9,
                        value=0.7,
                        step=0.05,
                        label="Train/Test Split Ratio",
                    )
                    cv_folds = gr.Number(
                        value=10,
                        label="Cross-Validation Folds",
                        precision=0,
                    )
                
                with gr.Accordion("Advanced Parameters", open=False):
                    gr.Markdown("Advanced configuration options will be added here.")
                
                setup_summary = gr.JSON(label="Setup Summary")
                initialize_btn = gr.Button("Initialize Setup", variant="primary")
                setup_status = gr.Markdown("")
            
            # Step 4: Compare Models
            with gr.Tab("Step 4: Compare Models"):
                gr.Markdown("### Compare All Available Models")
                compare_btn = gr.Button("Compare Models", variant="primary")
                compare_progress = gr.Markdown("")
                compare_results = gr.Dataframe(
                    label="Model Comparison Results",
                    interactive=True,
                )
                model_selection = gr.CheckboxGroup(
                    choices=[],
                    label="Select Models for Evaluation",
                )
            
            # Step 5: Evaluate Models
            with gr.Tab("Step 5: Evaluate Models"):
                gr.Markdown("### Evaluate Selected Models")
                model_selector = gr.Dropdown(
                    choices=[],
                    label="Select Model to Evaluate",
                )
                model_metrics = gr.JSON(label="Performance Metrics")
                plot_type = gr.Dropdown(
                    choices=[],
                    label="Select Plot Type",
                )
                plot_display = gr.Plot(label="Visualization")
                predictions_table = gr.Dataframe(label="Test Set Predictions")
            
            # Step 6: Export Model
            with gr.Tab("Step 6: Export Model"):
                gr.Markdown("### Export Your Trained Model")
                export_model_selector = gr.Dropdown(
                    choices=[],
                    label="Select Model to Export",
                )
                model_summary = gr.JSON(label="Model Summary")
                with gr.Row():
                    download_model_file = gr.File(label="Download Model (.pkl)", visible=False)
                    download_metadata_file = gr.File(label="Download Metadata (.json)", visible=False)
                download_model_btn = gr.Button("Download Model (.pkl)", variant="primary")
                download_metadata_btn = gr.Button("Download Metadata (.json)", variant="secondary")
                export_status = gr.Markdown("")
        
        # Event Handlers
        
        # Step 1: File Upload
        def process_upload(file, state):
            status, preview, stats, error = handle_file_upload(file, state, data_handler)
            return status, preview, stats
        
        file_upload.upload(
            fn=process_upload,
            inputs=[file_upload, state_component],
            outputs=[upload_status, data_preview, data_stats]
        )
        
        # Step 2: Problem Type Selection
        def process_problem_type(problem_type, state):
            description, choices = handle_problem_type_selection(problem_type, state, data_handler)
            return description, gr.update(choices=choices, value=None)
        
        problem_type.change(
            fn=process_problem_type,
            inputs=[problem_type, state_component],
            outputs=[problem_description, target_column]
        )
        
        # Target Column Selection
        def process_target(target_col, state):
            msg = handle_target_column_selection(target_col, state)
            return msg
        
        target_column.change(
            fn=process_target,
            inputs=[target_column, state_component],
            outputs=[gr.Markdown(visible=False)]  # Could add a status component
        )
        
        # Step 3: Setup Configuration
        def update_setup_summary(session_id, train_size, cv_folds, state):
            summary, status = handle_setup_configuration(
                session_id, train_size, cv_folds, state, config_manager
            )
            return summary, status
        
        session_id.change(
            fn=update_setup_summary,
            inputs=[session_id, train_size, cv_folds, state_component],
            outputs=[setup_summary, setup_status]
        )
        train_size.change(
            fn=update_setup_summary,
            inputs=[session_id, train_size, cv_folds, state_component],
            outputs=[setup_summary, setup_status]
        )
        cv_folds.change(
            fn=update_setup_summary,
            inputs=[session_id, train_size, cv_folds, state_component],
            outputs=[setup_summary, setup_status]
        )
        
        # Initialize Setup Button
        def initialize_setup(state):
            status = handle_setup_initialization(state, pycaret_wrapper, viz_manager)
            return status
        
        initialize_btn.click(
            fn=initialize_setup,
            inputs=[state_component],
            outputs=[setup_status]
        )
        
        # Step 4: Model Comparison
        def compare_all_models(state):
            results, status, choices = handle_model_comparison(state, pycaret_wrapper)
            return results, status, gr.update(choices=choices, value=[])
        
        compare_btn.click(
            fn=compare_all_models,
            inputs=[state_component],
            outputs=[compare_results, compare_progress, model_selection]
        )
        
        # Step 5: Model Evaluation
        def evaluate_model(model_name, state):
            metrics, plot_choices, status = handle_model_evaluation(
                model_name, state, pycaret_wrapper, viz_manager
            )
            return (
                metrics,
                gr.update(choices=plot_choices, value=None),
                ""
            )
        
        model_selector.change(
            fn=evaluate_model,
            inputs=[model_selector, state_component],
            outputs=[model_metrics, plot_type, gr.Markdown(visible=False)]
        )
        
        # Update model selector when models are selected
        def update_model_selector(selected_models, state):
            if selected_models:
                return gr.update(choices=selected_models, value=selected_models[0] if selected_models else None)
            return gr.update(choices=[], value=None)
        
        model_selection.change(
            fn=update_model_selector,
            inputs=[model_selection, state_component],
            outputs=[model_selector]
        )
        
        # Plot Generation
        def generate_plot(plot_type_val, state):
            plot, status = handle_plot_generation(plot_type_val, state, viz_manager)
            return plot, status
        
        plot_type.change(
            fn=generate_plot,
            inputs=[plot_type, state_component],
            outputs=[plot_display, gr.Markdown(visible=False)]
        )
        
        # Step 6: Model Export
        def prepare_export(model_name, state):
            summary, model_path, metadata_path = handle_model_export(model_name, state, model_manager)
            status_msg = f"✅ Model {model_name} ready for export!" if model_path else "❌ Export failed."
            return summary, status_msg
        
        export_model_selector.change(
            fn=prepare_export,
            inputs=[export_model_selector, state_component],
            outputs=[model_summary, export_status]
        )
        
        # Download buttons
        def download_model(model_name, state):
            if not model_name:
                return None
            summary, model_path, metadata_path = handle_model_export(model_name, state, model_manager)
            return model_path
        
        def download_metadata(model_name, state):
            if not model_name:
                return None
            summary, model_path, metadata_path = handle_model_export(model_name, state, model_manager)
            return metadata_path
        
        download_model_btn.click(
            fn=download_model,
            inputs=[export_model_selector, state_component],
            outputs=[download_model_file]
        )
        
        download_metadata_btn.click(
            fn=download_metadata,
            inputs=[export_model_selector, state_component],
            outputs=[download_metadata_file]
        )
        
        # Update export model selector when models are available
        def update_export_selector(selected_models, state):
            if selected_models:
                return gr.update(choices=selected_models, value=selected_models[0] if selected_models else None)
            return gr.update(choices=[], value=None)
        
        model_selection.change(
            fn=update_export_selector,
            inputs=[model_selection, state_component],
            outputs=[export_model_selector]
        )
        
        gr.Markdown("### Workflow Navigation")
        gr.Markdown("Use the tabs above to navigate through the workflow steps.")
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)

