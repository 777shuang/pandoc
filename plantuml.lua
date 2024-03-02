function Image(el)
    local pu = ".pu"
    if el.src:sub(-#pu) == pu then
        el.src = "svg-inkscape/" .. el.src .. ".svg"
    end
    return el
end