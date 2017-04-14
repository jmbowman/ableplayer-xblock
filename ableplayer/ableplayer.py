"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from django.template import Template, Context
from xblock.core import XBlock
from xblock.fields import Scope, String, List
from xblock.fragment import Fragment

class AblePlayerXBlock(XBlock):
    """
    Allows placement of a video accompanied by optional captions, chapters,
    and descriptive text.
    """
    title = String(default='Able Player Video', help="Title of your video")
    filepath = String(default=None, help="Path to your MP4 video file")
    description_files = List(default=None, help="Descriptive text VTT files")
    caption_files = List(default=None, help="Caption VTT files")
    chapter_files = List(default=None, help="Chapter VTT files")

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def build_fragment(self, context, template_path):
        """Build template fragment with the required assets"""
        if not context:
            context = {}

        context.update({
            'title': self.title,
            'filepath': self.filepath,
            'description_files': self.description_files,
            'caption_files': self.caption_files,
            'chapter_files': self.chapter_files
        })

        html = Template(
            self.resource_string(template_path)).render(Context(context))
        frag = Fragment(html)
        frag.add_css(self.resource_string("public/src/ableplayer.min.css"))
        frag.add_javascript(self.resource_string("public/vendor/modernizr.custom.js"))
        frag.add_javascript(self.resource_string("public/vendor/js.cookie.js"))
        frag.add_javascript(self.resource_string("public/src/ableplayer.min.js"))
        return frag

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the AblePlayerXBlock, shown to students
        when viewing courses.
        """
        # frag.add_resource(
        #     self.resource_string('public/src/button-icons/fonts/able.eot'),
        #     'application/vnd.ms-fontobject'
        # )
        # frag.add_resource(
        #     self.resource_string('public/src/button-icons/fonts/able.svg'),
        #     'image/svg+xml'
        # )
        # frag.add_resource(
        #     self.resource_string('public/src/button-icons/fonts/able.ttf'),
        #     'application/x-font-ttf',
        # )
        # frag.add_resource(
        #     self.resource_string('public/src/button-icons/fonts/able.woff'),
        #     'application/font-woff'
        # )

        return self.build_fragment(context, 'public/html/ableplayer.html')

    def studio_view(self, context=None):
        frag = self.build_fragment(context, 'public/html/ableplayer_edit.html')
        frag.add_javascript(self.resource_string('public/ableplayer_edit.js'))
        frag.initialize_js('AblePlayerEdit')
        return frag

    @XBlock.json_handler
    def edit_video_fields(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """

        self.title = data['title']
        self.filepath = data['filepath']
        if 'caption_files' in data:
            self.caption_files = data['caption_files']
        if 'description_files' in data:
            self.description_files = data['description_files']
        if 'chapter_files' in data:
            self.chapter_files = data['chapter_files']

        return {"response": 'success'}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("AblePlayerXBlock",
             """<ableplayer/>
             """),
            ("Multiple AblePlayerXBlock",
             """<vertical_demo>
                <ableplayer/>
                <ableplayer/>
                <ableplayer/>
                </vertical_demo>
             """),
        ]
