
[app]
title = Silo Management
package.name = silomanager
package.domain = org.test
version = 0.1

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy==2.3.0,requests,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.opengl_es2 = 1
android.hardware_acceleration = False
android.window_soft_input_mode = adjustResize

android.api = 31
android.minapi = 21
android.ndk_api = 21
android.build_tools_version = 31.0.0

# IMPORTANT: NDK 25+ only supports arm64
android.archs = arm64-v8a

p4a.bootstrap = sdl2
android.allow_backup = True

android.accept_sdk_license = True
android.skip_update = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer
