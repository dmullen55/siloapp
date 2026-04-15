[app]
# -------- App Info --------
title = Silo Management
package.name = silomanager
package.domain = org.test
version = 0.1

# -------- Source --------
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# -------- Python / Kivy --------
requirements = python3,kivy==2.3.0,requests,certifi
orientation = portrait
fullscreen = 0

# -------- Permissions --------
android.permissions = INTERNET

# -------- OpenGL / SDL --------
android.opengl_es2 = 1
android.hardware_acceleration = False
android.window_soft_input_mode = adjustResize

# -------- Android API Levels --------
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.build_tools_version = 31.0.0

# -------- Architectures (IMPORTANT) --------
# armeabi-v7a is NOT supported with NDK 25+
android.archs = arm64-v8a

# -------- SDK / NDK Paths --------
# Change ONLY if your SDK is elsewhere
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653
android.cmdline_tools_path = /usr/local/lib/android/sdk/cmdline-tools/latest

android.accept_sdk_license = True
android.skip_update = True

# -------- Bootstrap --------
p4a.bootstrap = sdl2
android.allow_backup = True

# -------- Buildozer --------
[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer
``
