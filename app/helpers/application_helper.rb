module ApplicationHelper
    def tab_item(name, url)
        opts = {}
        opts[:class] = 'current_page_item' if current_page?(url)
        content_tag :li, opts do
          link_to name, url
        end
    end
end
