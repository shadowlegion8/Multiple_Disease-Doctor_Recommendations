from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout as InnerBoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
import webbrowser
import pandas as pd
import os

class MyApp(App):
    def build(self):
        # Set the app title and icon
        self.title = 'Disease Prediction Dashboard'  # App name
        self.icon = 'icons.png'  # Path to your app icon

        layout = BoxLayout(orientation='vertical')

        # Add the logo
        logo = Image(source='doctor.png', size_hint=(1, 0.2))  # Adjust size_hint as needed
        layout.add_widget(logo)

        # Set the background color of the main layout
        layout.canvas.before.clear()
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.2, 0.6, 0.8, 1)  # Change this color to your preferred background color
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        # Add a label
        label = Label(text="Welcome to the Disease Prediction App", color=(1, 1, 1, 1))  # White text
        layout.add_widget(label)

        # Add a button to open the Streamlit app
        open_streamlit_button = Button(text="Open Streamlit App", background_color=(0.1, 0.5, 0.2, 1))  # Green button
        open_streamlit_button.bind(on_press=self.open_streamlit_app)
        layout.add_widget(open_streamlit_button)

        # Add a button to open the documentation page
        open_docs_button = Button(text="Open Documentation", background_color=(0.1, 0.5, 0.2, 1))  # Green button
        open_docs_button.bind(on_press=self.open_docs_page)
        layout.add_widget(open_docs_button)

        # Add a button for loading CSV files
        additional_feature_button = Button(text="Load CSV Files", background_color=(0.1, 0.5, 0.2, 1))  # Green button
        additional_feature_button.bind(on_press=self.additional_feature)
        layout.add_widget(additional_feature_button)

        # Add a button for an additional feature
        new_feature_button = Button(text="New Feature", background_color=(0.1, 0.5, 0.2, 1))  # Green button
        new_feature_button.bind(on_press=self.new_feature_method)
        layout.add_widget(new_feature_button)

        # Add a button to exit the app
        exit_button = Button(text="Exit", background_color=(0.8, 0.1, 0.1, 1))  # Red button
        exit_button.bind(on_press=self.stop)  # Calls the stop method to exit the app
        layout.add_widget(exit_button)

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def open_streamlit_app(self, instance):
        url = 'http://localhost:8501'
        webbrowser.open(url)

    def open_docs_page(self, instance):
        docs_url = 'http://your-documentation-url.com'
        webbrowser.open(docs_url)

    def additional_feature(self, instance):
        # Update the file path to use forward slashes or raw string
        csv_directory = r'D:/New folder/multiple-disease-prediction-streamlit-app-main/multiple-disease-prediction-streamlit-app-main/dataset'
        csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

        if csv_files:
            for csv_file in csv_files:
                file_path = os.path.join(csv_directory, csv_file)
                try:
                    df = pd.read_csv(file_path)
                    content = df.head(10).to_string()  # Display the first 10 rows for preview
                    self.display_csv_content(csv_file, content)
                except Exception as e:
                    print(f"Error reading {csv_file}: {e}")
        else:
            self.display_csv_content("No CSV files found", "")

    def display_csv_content(self, title, content):
        content_layout = BoxLayout(orientation='vertical')
        title_label = Label(text=f"Content of {title}", size_hint_y=None, height=40, color=(1, 1, 1, 1))  # White text
        content_label = Label(text=content, size_hint_y=None, height=400, text_size=(Window.width * 0.8, None), color=(1, 1, 1, 1))  # White text

        scroll_view = ScrollView(size_hint=(1, 1))
        inner_layout = InnerBoxLayout(orientation='vertical', size_hint_y=None)
        inner_layout.add_widget(title_label)
        inner_layout.add_widget(content_label)
        inner_layout.bind(minimum_height=inner_layout.setter('height'))
        scroll_view.add_widget(inner_layout)

        content_layout.add_widget(scroll_view)

        from kivy.uix.popup import Popup
        popup = Popup(title='CSV Content', content=content_layout, size_hint=(0.9, 0.9))
        popup.open()

    def new_feature_method(self, instance):
        print("New feature button clicked")

if __name__ == '__main__':
    Window.size = (400, 600)  # Optional: Set window size for better viewing
    MyApp().run()
