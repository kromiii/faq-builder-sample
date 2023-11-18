from jinja2 import Environment, FileSystemLoader

def generate_html(faq_items):
  env = Environment(loader=FileSystemLoader('.'))
  template = env.get_template('faq_template.html')
  html_content = template.render(faq_items=faq_items)
  return html_content