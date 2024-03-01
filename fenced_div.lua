if FORMAT:match 'html' then
    function Div(el)
        if #el.classes == 1 then
            -- insert element in front
            table.insert(el.content, 1, pandoc.RawBlock("html", "<div class='" .. el.classes[1] .. "'>"))
            -- insert element at the back
            table.insert(el.content, pandoc.RawBlock("html", "</div>"))
        end
        return el
    end
elseif FORMAT:match 'latex' then
    function Div(el)
        if #el.classes == 1 then
            -- insert element in front
            table.insert(el.content, 1, pandoc.RawBlock("latex", "\\begin{" .. el.classes[1] .. "}"))
            -- insert element at the back
            table.insert(el.content, pandoc.RawBlock("latex", "\\end{" .. el.classes[1] .. "}"))
        end
        return el
    end
end