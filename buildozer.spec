[app]
title = Silo Management
package.name = silomanager
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy==2.3.0,requests,certifi,urllib3,idna,chardet

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

# ---- OpenGL / SDL ----
android.opengl_es2 = 1
android.hardware_acceleration = False
android.window_soft_input_mode = adjustResize

# ---- Android API ----
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.build_tools_version = 31.0.0

# ---- SDK / NDK ----
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653
android.accept_sdk_license = True
android.skip_update = True

# ---- ARCHS (CRITICAL FIX) ----
android.archs = arm64-v8a,armeabi-v7a

# ---- Bootstrap ----
p4a.bootstrap = sdl2
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer
