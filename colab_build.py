# ============================================
# ZETA ANDROID APK BUILDER - COLAB VERSION
# ============================================
# Run this in Google Colab to build APK
#
# Steps:
# 1. Go to https://colab.research.google.com
# 2. Create New Notebook
# 3. Copy & paste this entire script
# 4. Run all cells
# ============================================

# ============================================
# STEP 1: INSTALL DEPENDENCIES
# ============================================
print("🔧 Installing system dependencies...")
!apt-get update -qq
!apt-get install -y -qq python3-dev python3-pip libg-dev libkivy-dev cmake git zip unzip openjdk-17-jdk
!pip install --upgrade pip -qq
!pip install kivy buildozer cython -qq
print("✅ Dependencies installed!")

# ============================================
# STEP 2: INSTALL ANDROID SDK
# ============================================
print("📱 Installing Android SDK...")
!mkdir -p /root/android-sdk

import os
os.environ['ANDROID_HOME'] = '/root/android-sdk'
os.environ['ANDROID_SDK_ROOT'] = '/root/android-sdk'
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-17-openjdk-amd64'

# Download command line tools
!wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/cmdline-tools.zip
!unzip -q -o /tmp/cmdline-tools.zip -d /tmp
!mkdir -p /root/android-sdk/cmdline-tools
!mv /tmp/cmdline-tools /root/android-sdk/cmdline-tools/latest 2>/dev/null || true

# Accept licenses
!yes | /root/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses > /dev/null 2>&1

# Install required SDK components
!/root/android-sdk/cmdline-tools/latest/bin/sdkmanager --install "platforms;android-33" "build-tools;33.0.2" "ndk;25b" "platform-tools" > /dev/null 2>&1

# Configure PATH
os.environ['PATH'] = f"{os.environ['PATH']}:/root/android-sdk/cmdline-tools/latest/bin:/root/android-sdk/platform-tools:/root/android-sdk/ndk/25b"

print("✅ Android SDK installed!")

# ============================================
# STEP 3: CLONE PROJECT FROM GITHUB
# ============================================
print("📥 Cloning project from GitHub...")
!git clone https://github.com/354ayam/zeta-android-app.git /content/zeta-app
%cd /content/zeta-app
!ls -la

# ============================================
# STEP 4: CREATE BUILD SPEC
# ============================================
print("⚙️ Creating build specification...")

buildozer_spec = '''[app]
title = Zeta App
package.name = zetaapp
package.domain = org.zeta
source.dir = .
version = 1.0.0
requirements = python3,kivy>=2.3.0
orientation = portrait
fullscreen = 1
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./.buildozer/bin

[kdroid]
android_api = 33
ndk_api = 25
'''

with open('buildozer.spec', 'w') as f:
    f.write(buildozer_spec)
print("✅ buildozer.spec created!")

# ============================================
# STEP 5: UPDATE MAIN.PY (if needed)
# ============================================
print("📝 Setting up main.py...")

main_py = '''"""
Zeta App - Python Android Application
Built with Kivy + Buildozer
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class ZetaApp(App):
    def build(self):
        # Set background color
        Window.clearcolor = (0.1, 0.1, 0.2, 1)

        # Main layout
        layout = BoxLayout(
            orientation='vertical',
            padding=50,
            spacing=20
        )

        # Title
        title = Label(
            text='[b]🚀 ZETA APP[/b]',
            markup=True,
            font_size='32sp',
            color=(0, 1, 0.5, 1),
            size_hint_y=0.2
        )

        # Description
        desc = Label(
            text='Aplikasi Android dengan Python + Kivy',
            font_size='16sp',
            color=(1, 1, 1, 1),
            size_hint_y=0.15
        )

        # Input field
        self.input_field = TextInput(
            hint_text='Ketik sesuatu...',
            multiline=False,
            size_hint_y=0.15,
            font_size='16sp'
        )

        # Button
        button = Button(
            text='[b]Klik Saya![/b]',
            markup=True,
            background_color=(0, 0.7, 1, 1),
            font_size='18sp',
            size_hint_y=0.2
        )
        button.bind(on_press=self.on_button_press)

        # Output label
        self.output = Label(
            text='Status: Siap ✅',
            font_size='14sp',
            color=(1, 1, 0, 1),
            size_hint_y=0.15
        )

        # Version info
        version = Label(
            text='v1.0.0 | Built with Kivy + Buildozer',
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.15
        )

        # Add widgets
        layout.add_widget(title)
        layout.add_widget(desc)
        layout.add_widget(self.input_field)
        layout.add_widget(button)
        layout.add_widget(self.output)
        layout.add_widget(version)

        return layout

    def on_button_press(self, instance):
        text = self.input_field.text or "Tanpa text"
        self.output.text = f'✅ Berhasil! Text: {text}'

if __name__ == '__main__':
    ZetaApp().run()
'''

with open('main.py', 'w') as f:
    f.write(main_py)
print("✅ main.py created!")

# ============================================
# STEP 6: BUILD APK
# ============================================
print("\n" + "="*50)
print("🔨 BUILDING APK...")
print("="*50)
print("⚠️ This will take 5-15 minutes...")
print("")

!buildozer android debug --verbose 2>&1 | tee build.log

print("\n" + "="*50)
print("🎉 BUILD COMPLETE!")
print("="*50)

# ============================================
# STEP 7: FIND & DOWNLOAD APK
# ============================================
import os
import glob

# Search for APK
apk_paths = glob.glob('/content/zeta-app/.buildozer/**/*.apk', recursive=True)

if apk_paths:
    print("\n📦 APK FOUND:")
    for apk in apk_paths:
        size = os.path.getsize(apk) / (1024*1024)
        print(f"   {apk} ({size:.2f} MB)")

    # Copy to main directory
    main_apk = apk_paths[0]
    !cp "{main_apk}" /content/zeta-app.apk

    print("\n" + "="*50)
    print("📥 DOWNLOAD APK:")
    print("/content/zeta-app.apk")
    print("="*50)

    # Download
    from google.colab import files
    files.download('/content/zeta-app.apk')
    print("\n✅ Check your downloads folder!")
else:
    print("\n❌ APK not found. Check build.log for errors.")
    print("\nLast 50 lines of build.log:")
    !tail -50 build.log
