[app]
title = Silo Manager
package.name = silomanager
package.domain = org.dmullen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Simplified requirements to ensure a clean build
requirements = python3,hostpython3,kivy==2.3.0,requests,certifi,openssl,urllib3,idna,charset-normalizer

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Let Buildozer manage the NDK and SDK versions automatically
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
p4a.bootstrap = sdl2
android.accept_sdk_license = True
android.uses_cleartext_traffic = True

[buildozer]
log_level = 2
warn_on_root = 1
