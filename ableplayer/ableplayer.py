"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblockutils.settings import XBlockWithSettingsMixin, ThemableXBlockMixin

class ResourceMixin(XBlockWithSettingsMixin, ThemableXBlockMixin):
    loader = ResourceLoader(__name__)

    block_settings_key = 'ableplayer-xblock'
    default_theme_config = {
        'package': 'ableplayer-xblock',
        'locations': [
            'public/ableplayer.min.css',
            'public/ableplayer.min.js'
        ]
    }

    # @staticmethod
    # def resource_string(path):
    #     """Handy helper for getting resources from our kit."""
    #     data = pkg_resources.resource_string(__name__, path)
    #     return data.decode("utf8")

    # def create_fragment(self, context, template, css, js, js_init):
    #     html = Template(
    #         self.resource_string(template)).render(Context(context))
    #     frag = Fragment(html)
    #     frag.add_javascript_url(
    #         self.runtime.local_resource_url(
    #             self, 'public/js/vendor/handlebars.js'))
    #     frag.add_css(self.resource_string(css))
    #     frag.add_javascript(self.resource_string(js))
    #     frag.initialize_js(js_init)
    #     self.include_theme_files(frag)
    #     return frag

class AblePlayerXBlock(XBlock, ResourceMixin):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the AblePlayerXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/ableplayer.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("public/src/ableplayer.min.css"))
        frag.add_javascript(self.resource_string("public/vendor/modernizr.custom.js"))
        frag.add_javascript(self.resource_string("public/vendor/js.cookie.js"))
        frag.add_javascript(self.resource_string("public/src/ableplayer.min.js"))
        frag.initialize_js('AblePlayerXBlock')
        return frag

    def studio_view(self, context=None):
        html = self.resource_string("static/html/ableplayer.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/ableplayer.css"))
        frag.add_javascript(self.resource_string("static/js/src/ableplayer.js"))
        frag.initialize_js('AblePlayerXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

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
