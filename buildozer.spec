[app]

# Force GLES2 (disable ES3 which crashes silently)
android.opengl_es2 = 1
android.opengl_es3 = 0

# Disable hardware acceleration (prevents SDL crashes)
android.hardware_acceleration = False

# Prevent surface resize crash during startup
android.window_soft_input_mode = adjustResize

title = Silo Management
package.name = silomanager
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy==2.3.0,requests,certifi

orientation = portrait
fullscreen = 0

android.permissions = android.permission.INTERNET

# ---------- ANDROID CONFIG (CRITICAL FIXES) ----------
android.api = 31
android.minapi = 21
android.ndk_api = 21

# Pin exact versions to avoid license prompts & AIDL errors
android.build_tools_version = 31.0.0
android.ndk = 25b

# ✅ Force Buildozer to use the SDK we install in GitHub Actions
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653

# Prevent Buildozer from trying to download/upate SDK components
android.accept_sdk_license = True
android.skip_update = True

android.archs = armeabi-v7a
p4a.bootstrap = sdl2
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer

