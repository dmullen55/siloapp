[app]
title = Silo Manager
package.name = silomanager
package.domain = org.dmullen
version = 0.1
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
android.manifest.application_extra_xml = <uses-native-library android:name="libcrypto.so" android:required="false" /> <uses-native-library android:name="libssl.so" android:required="false" />

# CRITICAL: Added openssl and supporting libraries for Supabase
requirements = python3,kivy==2.3.0,requests,certifi,openssl,urllib3,charset-normalizer,idna

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Modern API levels for 2026 compatibility
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
p4a.bootstrap = sdl2
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer
