# Legacy Files

This directory contains files from the original Prism AI Voice Assistant implementation that have been replaced by the new modular structure.

## Files in this directory:

### Core Files (Replaced)
- **`prism_features.py`**: Original monolithic features file - now split into individual service modules in `prism/features/`
- **`demo_prism.py`**: Demo version of the app - functionality now integrated into main app
- **`install_prism.py`**: Installation script - setup now handled by `scripts/setup_features.py`

### Test Files (Replaced)
- **`test_whisper_simple.py`**: Whisper API testing - no longer needed
- **`test_openai_whisper.py`**: OpenAI Whisper testing - no longer needed
- **`simple_voice_test.py`**: Voice testing - functionality now in main app
- **`debug_audio.py`**: Audio debugging - debugging now handled in main app
- **`test_openai_models.py`**: OpenAI model testing - no longer needed
- **`test_google_speech.py`**: Google Speech testing - no longer needed
- **`test_api_status.py`**: API status testing - no longer needed
- **`test_prism.py`**: General testing - replaced by `tests/test_features.py`

### Utility Files (Replaced)
- **`enable_google_apis.py`**: Google API setup - now documented in `docs/google_cloud_setup.md`

## Migration Notes

These files are kept for reference and can be safely deleted if no longer needed. The new modular structure in the `prism/` directory provides:

1. **Better Organization**: Features are now in separate, focused modules
2. **Improved Maintainability**: Each service is self-contained
3. **Enhanced Testability**: Individual components can be tested in isolation
4. **Better Scalability**: New features can be added easily

## Current Structure

The new structure uses:
- `prism/features/` for individual feature services
- `prism/core/` for core application components
- `tests/` for test files
- `scripts/` for utility scripts
- `docs/` for documentation

All functionality from these legacy files has been preserved and improved in the new structure. 