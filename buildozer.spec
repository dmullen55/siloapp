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

android.api = 31
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a
p4a.bootstrap = sdl2

android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
