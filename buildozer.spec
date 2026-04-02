[app]

title = Silo Management
package.name = silomanager
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy,requests

orientation = portrait
fullscreen = 0

android.permissions = android.permission.INTERNET

# ---------- ANDROID CONFIG (CRITICAL FIXES) ----------
android.api = 31
android.minapi = 21
android.ndk_api = 21

# Pin exact versions to avoid license prompts & AIDL errors
android.build_tools_version = 31.0.0
android.ndk = 23.1.7779620

# ✅ Force Buildozer to use the SDK we install in GitHub Actions
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/23.1.7779620

# Prevent Buildozer from trying to download/upate SDK components
android.accept_sdk_license = True
android.skip_update = True

android.archs = arm64-v8a
p4a.bootstrap = sdl2
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer
``
