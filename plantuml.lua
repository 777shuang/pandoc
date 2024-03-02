local dirname = function(str)
	if str:match(".-/.-") then
		local name = string.gsub(str, "(.*/)(.*)", "%1")
		return name
	else
		return ''
	end
end

local basename = function(str)
	local name = string.gsub(str, "(.*/)(.*)", "%2")
	return name
end

function Image(el)
    local pu = ".pu"
    if el.src:sub(-#pu) == pu then
        el.src = dirname(el.src) .. "svg-inkscape/" .. basename(el.src) .. ".svg"
    end
    return el
end