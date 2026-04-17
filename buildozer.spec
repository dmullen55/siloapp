[app]
title = Silo Manager [cite: 1]
package.name = silomanager [cite: 1]
package.domain = org.dmullen [cite: 1]
source.dir = . [cite: 1]
source.include_exts = py,png,jpg,kv,atlas [cite: 2]
version = 0.1

# Essential for Kivy + Requests + Supabase
requirements = python3,hostpython3,kivy==2.3.0,requests,certifi,openssl,urllib3,idna,charset-normalizer

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Standard API levels for 2026 compatibility
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
p4a.bootstrap = sdl2
android.accept_sdk_license = True
android.uses_cleartext_traffic = True

[buildozer]
log_level = 2
warn_on_root = 1
# This ensures the APK ends up in the folder the YAML is looking for
bin_dir = ./bin
