from app import app
from markdown import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

class AfterRenderExtension(Extension):
	def extendMarkdown(self, md, md_globals):
		treeprocessor = AfterRenderTreeProcessor(md)
		treeprocessor.ext = self
		md.treeprocessors['afterrender'] = treeprocessor

class AfterRenderTreeProcessor(Treeprocessor):

	def run (self, root):
		for plugin in app.plugins.values():
			root = plugin.after_render(root)
		return root
