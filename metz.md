.
├── README.md
├── Specifications
│   ├── Module_01_Global_Constants.md
│   ├── Module_03_Entities.md
│   ├── Technical_Design_Document_4_SuperManim.md
│   └── zipy_info_source.md
├── adapters
│   ├── __init__.py
│   ├── cli
│   │   ├── __init__.py
│   │   ├── cli_audio_command.py
│   │   ├── cli_export_command.py
│   │   ├── cli_project_command.py
│   │   ├── cli_render_command.py
│   │   ├── cli_scene_command.py
│   │   ├── command_parser.py
│   │   ├── output_formatter.py
│   │   └── shell.py
│   ├── gui
│   │   └── __init__.py
│   ├── infrastructure
│   │   ├── __init__.py
│   │   ├── file
│   │   │   ├── __init__.py
│   │   │   ├── local_file_storage.py
│   │   │   └── sha256_hash_computer.py
│   │   └── system
│   │       ├── __init__.py
│   │       ├── asset_manager.py
│   │       └── temp_file_manager.py
│   ├── media
│   │   ├── __init__.py
│   │   ├── ffmpeg
│   │   │   ├── __init__.py
│   │   │   ├── ffmpeg_audio_processor.py
│   │   │   └── ffmpeg_video_assembler.py
│   │   ├── librosa
│   │   │   ├── __init__.py
│   │   │   └── librosa_audio_analyzer.py
│   │   ├── manim
│   │   │   ├── __init__.py
│   │   │   └── manim_render_runner.py
│   │   └── preview
│   │       ├── __init__.py
│   │       └── fast_preview_generator.py
│   ├── notification
│   │   ├── __init__.py
│   │   ├── cli
│   │   │   ├── __init__.py
│   │   │   ├── cli_logger.py
│   │   │   ├── cli_notification.py
│   │   │   └── cli_progress_reporter.py
│   │   ├── gui
│   │   │   ├── __init__.py
│   │   │   ├── gui_logger.py
│   │   │   ├── gui_notification.py
│   │   │   └── gui_progress_reporter.py
│   │   └── web
│   │       ├── __init__.py
│   │       ├── web_logger.py
│   │       ├── web_notification.py
│   │       └── web_progress_reporter.py
│   └── repositories
│       ├── __init__.py
│       ├── in_memory
│       │   └── __init__.py
│       ├── json
│       │   └── __init__.py
│       └── sqlite
│           ├── __init__.py
│           ├── sqlite_audio_repository.py
│           ├── sqlite_cache_repository.py
│           ├── sqlite_project_repository.py
│           ├── sqlite_project_settings_repository.py
│           ├── sqlite_render_history_repository.py
│           ├── sqlite_scene_repository.py
│           └── sqlite_session_repository.py
├── application
│   ├── __init__.py
│   └── use_case
│       ├── __init__.py
│       ├── app_state_service.py
│       ├── audio_service.py
│       ├── export_service.py
│       ├── preview_service.py
│       ├── project_service.py
│       ├── render_service.py
│       ├── scene_service.py
│       ├── session_service.py
│       └── sync_service.py
├── bootstrap.py
├── config
│   ├── __init__.py
│   └── constants.py
├── core
│   ├── __init__.py
│   ├── domain_exception.py
│   ├── entities
│   │   ├── __init__.py
│   │   ├── asset_file.py
│   │   ├── audio_clip.py
│   │   ├── audio_file.py
│   │   ├── audio_settings.py
│   │   ├── export_settings.py
│   │   ├── preview_settings.py
│   │   ├── project.py
│   │   ├── project_settings.py
│   │   ├── render_settings.py
│   │   ├── scenes.py
│   │   ├── timeline.py
│   │   ├── video_clip.py
│   │   ├── video_file.py
│   │   └── video_settings.py
│   ├── ports
│   │   ├── __init__.py
│   │   ├── driving_ports
│   │   │   ├── __init__.py
│   │   │   ├── audio_command_port.py
│   │   │   ├── export_command_port.py
│   │   │   ├── project_command_port.py
│   │   │   ├── render_command_port.py
│   │   │   └── scene_command_port.py
│   │   ├── infrastructure_ports
│   │   │   ├── __init__.py
│   │   │   ├── asset_manager_port.py
│   │   │   ├── file_storage_port.py
│   │   │   ├── hash_computer_port.py
│   │   │   └── temp_file_manager_port.py
│   │   ├── media_processing_ports
│   │   │   ├── __init__.py
│   │   │   ├── audio_analyzer_port.py
│   │   │   ├── audio_processor_port.py
│   │   │   ├── preview_generator_port.py
│   │   │   ├── render_runner_port.py
│   │   │   └── video_assembler_port.py
│   │   ├── notification_ports
│   │   │   ├── __init__.py
│   │   │   ├── logger_port.py
│   │   │   ├── notification_port.py
│   │   │   └── progress_reporter_port.py
│   │   └── repository_ports
│   │       ├── __init__.py
│   │       ├── audio_repository_port.py
│   │       ├── cache_repository_port.py
│   │       ├── project_repository_port.py
│   │       ├── project_settings_repository_port.py
│   │       ├── render_history_repository_port.py
│   │       ├── scene_repository_port.py
│   │       └── session_repository_port.py
│   └── services
│       ├── __init__.py
│       ├── audio_validation_service.py
│       ├── hash_service.py
│       ├── project_validation_service.py
│       ├── scene_validation_service.py
│       └── timeline_service.py
├── database
│   └── connection.py
├── main.py
├── metz.md
├── requirements.txt
├── tests
│   └── __init__.py
└── utils
    ├── __init__.py
    └── utilities.py

36 directories, 131 files
