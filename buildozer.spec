[app]
title = Silo Manager
package.name = silomanager
package.domain = org.dmullen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# hostpython3 is REQUIRED for the build process to complete
requirements = python3,hostpython3,kivy==2.3.0,requests,certifi,openssl,urllib3,charset-normalizer,idna

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
p4a.bootstrap = sdl2
android.accept_sdk_license = True

# Allows the app to bypass strict SSL/DNS issues during testing
android.uses_cleartext_traffic = True

[buildozer]
log_level = 2
warn_on_root = 1
