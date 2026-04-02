"""
Interactive Shell Module
========================
The main REPL (Read-Eval-Print-Loop) for SuperManim.
Reads user input, parses commands, dispatches to the appropriate service,
and formats the output.
"""

from __future__ import annotations

import cmd
import os
import shutil

from config.constants import CLI_PROMPT

from adapters.cli.command_parser import CommandParser
from adapters.cli.output_formatter import OutputFormatter
from adapters.cli.cli_project_command import CLIProjectCommand
from adapters.cli.cli_scene_command import CLISceneCommand
from adapters.cli.cli_audio_command import CLIAudioCommand
from adapters.cli.cli_render_command import CLIRenderCommand
from adapters.cli.cli_export_command import CLIExportCommand


class SuperManimShell(cmd.Cmd):
    """Interactive command-line shell for SuperManim.

    Provides a REPL that reads user commands, dispatches them to the
    appropriate application service, and displays formatted results.

    Usage:
        shell = SuperManimShell(services_container)
        shell.cmdloop()
    """

    def __init__(self, services_container: dict) -> None:
        """Initialize with all application services.

        Args:
            services_container: A dict with keys:
                'project_service', 'scene_service', 'audio_service',
                'render_service', 'sync_service', 'export_service',
                'preview_service', 'app_state_service',
                'logger', 'notifier', 'progress_reporter',
                'file_storage', 'project_repos', 'asset_manager'.
        """
        super().__init__()

        self.services = services_container
        self.parser = CommandParser()
        self.formatter = OutputFormatter()
        self.prompt = CLI_PROMPT

        # Shortcuts to frequently-used services
        self._notifier = services_container.get("notifier")
        self._logger = services_container.get("logger")
        self._file_storage = services_container.get("file_storage")

        # Initialize CLI command adapters
        self._project_cmd = CLIProjectCommand(
            project_service=services_container.get("project_service"),
            app_state_service=services_container.get("app_state_service"),
            formatter=self.formatter,
            notifier=self._notifier,
        )
        self._scene_cmd = CLISceneCommand(
            scene_service=services_container.get("scene_service"),
            formatter=self.formatter,
            notifier=self._notifier,
        )
        self._audio_cmd = CLIAudioCommand(
            audio_service=services_container.get("audio_service"),
            formatter=self.formatter,
            notifier=self._notifier,
        )
        self._render_cmd = CLIRenderCommand(
            render_service=services_container.get("render_service"),
            preview_service=services_container.get("preview_service"),
            formatter=self.formatter,
            notifier=self._notifier,
            progress=services_container.get("progress_reporter"),
        )
        self._export_cmd = CLIExportCommand(
            export_service=services_container.get("export_service"),
            formatter=self.formatter,
            notifier=self._notifier,
            file_storage=self._file_storage,
        )

    # ------------------------------------------------------------------
    # cmd.Cmd overrides
    # ------------------------------------------------------------------

    def precmd(self, line: str) -> str:
        """Strip leading whitespace before processing."""
        return line.strip()

    def postcmd(self, stop: bool, line: str) -> bool:
        """Return the stop flag after each command."""
        return stop

    def default(self, line: str) -> None:
        """Handle all unrecognized commands via the parser.

        This is the main dispatch method: every user command flows through
        here, gets parsed, and is routed to the appropriate handler.
        """
        action, args = self.parser.parse(line)
        if action != "unknown":
            self._dispatch(action, args)

    def emptyline(self) -> None:
        """Do nothing on empty input (do not repeat the last command)."""
        pass

    def do_exit(self, _line: str) -> bool:
        """Exit the shell."""
        self._notifier.notify_info("Goodbye!")
        return True

    def do_quit(self, _line: str) -> bool:
        """Exit the shell (alias for exit)."""
        return self.do_exit(_line)

    def do_q(self, _line: str) -> bool:
        """Exit the shell (short alias)."""
        return self.do_exit(_line)

    def postloop(self) -> None:
        """Called after the REPL loop ends."""
        print()

    def intro(self) -> str:
        """Return the intro message displayed when cmdloop starts."""
        return self.formatter.format_welcome()

    # ------------------------------------------------------------------
    # Main dispatch method
    # ------------------------------------------------------------------

    def _dispatch(self, action: str, args: list[str]) -> None:
        """Route the parsed command to the appropriate handler.

        Commands that require an open project are guarded with a check.
        Each handler is responsible for calling the service, formatting
        the result, and printing it.

        Args:
            action: The canonical action string from the parser.
            args: The remaining argument tokens.
        """
        # ---- Project commands (no project required) ----

        if action == "new project":
            self._project_cmd.handle_new(args)
            self._on_project_opened()
            return

        if action == "open project":
            self._project_cmd.handle_open(args)
            self._on_project_opened()
            return

        if action == "close project":
            self._project_cmd.handle_close(args)
            self._on_project_closed()
            return

        if action == "delete project":
            self._project_cmd.handle_delete(args)
            return

        if action == "rename project":
            self._require_project(self._project_cmd.handle_rename, args)
            return

        if action == "list projects":
            self._project_cmd.handle_list()
            return

        if action == "project info":
            self._project_cmd.handle_info()
            return

        if action == "export project":
            self._require_project(self._project_cmd.handle_export)
            return

        if action == "status":
            self._project_cmd.handle_status()
            return

        # ---- Scene commands (require project) ----

        if action == "set scenes_number":
            self._require_project(self._scene_cmd.handle_set_scenes_number, args)
            return

        if action == "list scenes":
            self._require_project(self._scene_cmd.handle_list)
            return

        if action.startswith("set scene") and "duration" in action:
            self._require_project(self._scene_cmd.handle_set_duration, args)
            return

        if action.startswith("set scene") and "code" in action:
            self._require_project(self._scene_cmd.handle_set_code, args)
            return

        if action.startswith("set scene") and "fps" in action:
            self._require_project(self._scene_cmd.handle_set_fps, args)
            return

        if action.startswith("set scene") and "width" in action:
            self._require_project(self._scene_cmd.handle_set_width, args)
            return

        if action.startswith("set scene") and "height" in action:
            self._require_project(self._scene_cmd.handle_set_height, args)
            return

        if action.startswith("set scene") and "audio" in action:
            self._require_project(self._scene_cmd.handle_set_audio, args)
            return

        if action == "delete scene":
            self._require_project(self._scene_cmd.handle_delete, args)
            return

        if action == "duplicate scene":
            self._require_project(self._scene_cmd.handle_duplicate, args)
            return

        if action == "move scene":
            self._require_project(self._scene_cmd.handle_move, args)
            return

        if action == "merge scenes":
            self._require_project(self._scene_cmd.handle_merge, args)
            return

        if action == "reset scene":
            self._require_project(self._scene_cmd.handle_reset, args)
            return

        if action == "reset all scenes":
            self._require_project(self._scene_cmd.handle_reset_all)
            return

        # ---- Audio commands (require project) ----

        if action == "add audio":
            self._require_project(self._audio_cmd.handle_add, args)
            return

        if action == "add video":
            self._require_project(self._audio_cmd.handle_add_video, args)
            return

        if action == "add asset":
            self._handle_add_asset(args)
            return

        if action == "split audio silence":
            self._require_project(self._audio_cmd.handle_split_silence)
            return

        if action == "split audio":
            self._require_project(self._audio_cmd.handle_split, args)
            return

        if action == "convert audio":
            self._require_project(self._audio_cmd.handle_convert, args)
            return

        if action == "trim audio":
            self._require_project(self._audio_cmd.handle_trim, args)
            return

        if action == "trim video":
            self._require_project(self._audio_cmd.handle_trim_video, args)
            return

        if action == "remove audio from video":
            self._require_project(self._audio_cmd.handle_remove_from_video)
            return

        if action == "extract audio from video":
            self._require_project(self._audio_cmd.handle_extract_from_video)
            return

        if action == "merge audio":
            self._require_project(self._audio_cmd.handle_merge, args)
            return

        if action == "list audio":
            self._require_project(self._audio_cmd.handle_list_audio)
            return

        if action == "list video":
            self._require_project(self._audio_cmd.handle_list_video)
            return

        if action == "list assets":
            self._require_project(self._handle_list_assets)
            return

        if action == "delete audio":
            self._require_project(self._audio_cmd.handle_delete_audio, args)
            return

        if action == "delete video":
            self._require_project(self._audio_cmd.handle_delete_video, args)
            return

        if action == "set active audio":
            self._require_project(self._audio_cmd.handle_set_active_audio, args)
            return

        if action == "set active video":
            self._require_project(self._audio_cmd.handle_set_active_video, args)
            return

        # ---- Render commands (require project) ----

        if action == "render scene":
            self._require_project(self._render_cmd.handle_render_scene, args)
            return

        if action == "render all":
            self._require_project(self._render_cmd.handle_render_all)
            return

        if action == "render pending":
            self._require_project(self._render_cmd.handle_render_pending)
            return

        if action == "preview scene":
            self._require_project(self._render_cmd.handle_preview_scene, args)
            return

        if action == "preview all":
            self._require_project(self._render_cmd.handle_preview_all)
            return

        if action == "check dependencies":
            self._render_cmd.handle_check_deps()
            return

        # ---- Export commands (require project) ----

        if action == "export":
            self._require_project(self._export_cmd.handle_export)
            return

        if action == "export scene":
            self._require_project(self._export_cmd.handle_export_scene, args)
            return

        if action == "delete output":
            self._handle_delete_output()
            return

        # ---- Sync commands (require project) ----

        if action == "sync all":
            self._handle_sync_all()
            return

        # ---- General commands ----

        if action == "help":
            print(self.formatter.format_help())
            return

        if action == "clear":
            self._clear_screen()
            return

        if action == "set default fps":
            self._handle_set_default_fps(args)
            return

        # ---- Unknown command ----
        print(self.formatter.format_error(f"Unknown command: {action}"))
        print(self.formatter.format_info("Type 'help' for available commands."))

    # ------------------------------------------------------------------
    # Guard helpers
    # ------------------------------------------------------------------

    def _require_project(self, handler, *args) -> None:
        """Check that a project is open before calling the handler.

        If no project is open, prints a warning and returns without
        calling the handler.

        Args:
            handler: Callable to invoke if a project is open.
            *args: Arguments to pass to the handler.
        """
        if not self._project_cmd.is_project_open():
            print(self.formatter.format_warning(
                "No project is currently open. "
                "Use 'new project <name>' or 'open project <name>' first."
            ))
            return
        handler(*args)

    # ------------------------------------------------------------------
    # Project lifecycle helpers
    # ------------------------------------------------------------------

    def _on_project_opened(self) -> None:
        """Initialize project-scoped services after a project is opened.

        Called after 'new project' and 'open project' commands succeed.
        Sets the project path on scene_service, audio_service, render_service,
        export_service, preview_service, and sync_service.  Also initializes
        the project-scoped repositories.
        """
        state = self.services["app_state_service"].get_current_state()
        project_path = state.get("last_project_path", "")

        if not project_path:
            return

        # Initialize project-scoped repositories
        project_repos = self.services.get("project_repos")
        if project_repos and hasattr(project_repos, "initialize"):
            project_repos.initialize(project_path)

        # Set project path AND inject project-scoped repos on all services
        scene_service = self.services.get("scene_service")
        audio_service = self.services.get("audio_service")
        render_service = self.services.get("render_service")
        export_service = self.services.get("export_service")
        preview_service = self.services.get("preview_service")
        sync_service = self.services.get("sync_service")

        if scene_service and hasattr(scene_service, "set_project_path"):
            scene_service.set_project_path(project_path)
            # Inject the project-scoped repos into the service
            scene_service._scene_repo = project_repos.scene_repo
            scene_service._cache_repo = project_repos.cache_repo

        if audio_service and hasattr(audio_service, "set_project_path"):
            audio_service.set_project_path(project_path)
            audio_service._audio_repo = project_repos.audio_repo

        if render_service and hasattr(render_service, "set_project_path"):
            render_service.set_project_path(project_path)
            render_service._scene_repo = project_repos.scene_repo
            render_service._cache_repo = project_repos.cache_repo
            render_service._render_history_repo = project_repos.render_history_repo

        if export_service and hasattr(export_service, "set_project_path"):
            export_service.set_project_path(project_path)
            export_service._scene_repo = project_repos.scene_repo
            export_service._audio_repo = project_repos.audio_repo

        if preview_service and hasattr(preview_service, "set_project_path"):
            preview_service.set_project_path(project_path)
            preview_service._scene_repo = project_repos.scene_repo

        if sync_service and hasattr(sync_service, "set_project_path"):
            sync_service.set_project_path(project_path)
            sync_service._scene_repo = project_repos.scene_repo
            sync_service._audio_repo = project_repos.audio_repo

        # Update CLI command adapters with refreshed services
        self._scene_cmd = CLISceneCommand(
            scene_service=scene_service,
            formatter=self.formatter,
            notifier=self._notifier,
        )
        self._audio_cmd = CLIAudioCommand(
            audio_service=audio_service,
            formatter=self.formatter,
            notifier=self._notifier,
        )
        self._render_cmd = CLIRenderCommand(
            render_service=render_service,
            preview_service=preview_service,
            formatter=self.formatter,
            notifier=self._notifier,
            progress=self.services.get("progress_reporter"),
        )
        self._export_cmd = CLIExportCommand(
            export_service=export_service,
            formatter=self.formatter,
            notifier=self._notifier,
            file_storage=self._file_storage,
        )

    def _on_project_closed(self) -> None:
        """Reset project-scoped services after a project is closed."""
        pass

    # ------------------------------------------------------------------
    # Special command handlers
    # ------------------------------------------------------------------

    def _handle_add_asset(self, args: list[str]) -> None:
        """Handle 'add asset <path>' command.

        Copies an asset file into the project's assets directory.

        Args:
            args: List with the asset file path.
        """
        if not args:
            print(self.formatter.format_error("Usage: add asset <path>"))
            return

        state = self.services["app_state_service"].get_current_state()
        project_path = state.get("last_project_path", "")
        if not project_path:
            print(self.formatter.format_warning("No project is open."))
            return

        asset_path = args[0]
        asset_manager = self.services.get("asset_manager")
        if asset_manager is None:
            print(self.formatter.format_error("Asset manager not available."))
            return

        # Determine asset type from file extension
        ext = os.path.splitext(asset_path)[1].lstrip(".").lower()
        asset_type_map = {
            "mp3": "audio", "wav": "audio", "ogg": "audio", "flac": "audio",
            "aac": "audio", "m4a": "audio", "mp4": "videos", "mov": "videos",
            "mkv": "videos", "avi": "videos", "webm": "videos",
            "png": "images", "jpg": "images", "jpeg": "images", "gif": "images",
            "svg": "images", "ttf": "fonts", "otf": "fonts", "woff": "fonts",
        }
        asset_type = asset_type_map.get(ext, "images")

        try:
            result = asset_manager.store_asset(asset_path, project_path, asset_type)
            print(self.formatter.format_success(
                f"Asset '{result['name']}' added to {asset_type}/."
            ))
            print(f"  Path: {result['file_path']}")
        except FileNotFoundError:
            print(self.formatter.format_error(f"File not found: '{asset_path}'"))
        except Exception as exc:
            print(self.formatter.format_error(f"Failed to add asset: {exc}"))

    def _handle_list_assets(self) -> None:
        """Handle 'list assets' command."""
        state = self.services["app_state_service"].get_current_state()
        project_path = state.get("last_project_path", "")
        if not project_path:
            print(self.formatter.format_warning("No project is open."))
            return

        asset_manager = self.services.get("asset_manager")
        if asset_manager is None:
            print(self.formatter.format_error("Asset manager not available."))
            return

        try:
            assets = asset_manager.list_assets(project_path)
            if not assets:
                print(self.formatter.format_info("No assets found."))
                return

            lines = [self.formatter.format_separator(), "  Assets", self.formatter.format_separator()]
            for asset in assets:
                name = asset.get("name", "unknown")
                asset_type = asset.get("asset_type", "?")
                file_path = asset.get("file_path", "")
                lines.append(f"  [{asset_type:<8}] {name:<30}")
                lines.append(f"             {file_path}")
            lines.append(self.formatter.format_separator())
            print("\n".join(lines))
        except Exception as exc:
            print(self.formatter.format_error(f"Failed to list assets: {exc}"))

    def _handle_delete_output(self) -> None:
        """Handle 'delete output' command.

        Removes the contents of the project's output directory.
        """
        state = self.services["app_state_service"].get_current_state()
        project_path = state.get("last_project_path", "")
        if not project_path:
            print(self.formatter.format_warning("No project is open."))
            return

        output_dir = os.path.join(project_path, "output")
        if not os.path.isdir(output_dir):
            print(self.formatter.format_info("No output directory found."))
            return

        try:
            for entry in os.listdir(output_dir):
                entry_path = os.path.join(output_dir, entry)
                if os.path.isfile(entry_path):
                    os.remove(entry_path)
                elif os.path.isdir(entry_path):
                    shutil.rmtree(entry_path)
            print(self.formatter.format_success("Output directory cleared."))
        except Exception as exc:
            print(self.formatter.format_error(f"Failed to delete output: {exc}"))

    def _handle_sync_all(self) -> None:
        """Handle 'sync all' command."""
        if not self._project_cmd.is_project_open():
            print(self.formatter.format_warning(
                "No project is currently open. "
                "Use 'new project <name>' or 'open project <name>' first."
            ))
            return

        sync_service = self.services.get("sync_service")
        if sync_service is None:
            print(self.formatter.format_error("Sync service not available."))
            return

        result = sync_service.sync_all()
        if result.get("success"):
            data = result.get("data", {}) or {}
            print(self.formatter.format_sync_status(data))
        else:
            print(self.formatter.format_error(result.get("message", "Sync failed.")))

    def _handle_set_default_fps(self, args: list[str]) -> None:
        """Handle 'set default fps <x>' command.

        Updates the project settings with a new default FPS value.

        Args:
            args: List with the FPS value.
        """
        if not args:
            print(self.formatter.format_error("Usage: set default fps <x>"))
            return

        if not self._project_cmd.is_project_open():
            print(self.formatter.format_warning("No project is open."))
            return

        try:
            fps = int(args[0])
        except ValueError:
            print(self.formatter.format_error("FPS must be an integer."))
            return

        settings_repo = self.services.get("project_repos")
        if settings_repo and hasattr(settings_repo, "settings_repo") and settings_repo.settings_repo:
            try:
                settings_repo.settings_repo.update_settings({"render_fps": fps})
                print(self.formatter.format_success(f"Default FPS set to {fps}."))
            except Exception as exc:
                print(self.formatter.format_error(f"Failed to update settings: {exc}"))
        else:
            print(self.formatter.format_warning(
                "Cannot update settings: project repositories not initialized."
            ))

    @staticmethod
    def _clear_screen() -> None:
        """Clear the terminal screen."""
        # ANSI escape sequence to clear the screen and move cursor to top
        print("\033[2J\033[H", end="")
