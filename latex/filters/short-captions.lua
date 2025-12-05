-- https://github.com/pandoc/lua-filters/tree/master/short-captions
io.stderr:write("short-captions.lua is running\n")

if FORMAT ~= "latex" then
	return
end

function Figure(fig)
	local img = nil

	if fig.content[1] then
		local first = fig.content[1]
		if first.t == "Plain" and first.content[1] and first.content[1].t == "Image" then
			img = first.content[1]
		elseif first.t == "Image" then
			img = first
		end
	end

	if not img then
		return nil
	end

	local short = img.attributes["short-caption"]
	if not short then
		return nil
	end

	local long_caption = pandoc.write(pandoc.Pandoc({ pandoc.Para(fig.caption.long[1].content) }), "latex")

	local label = ""
	if fig.identifier and fig.identifier ~= "" then
		label = string.format("\\label{%s}", fig.identifier)
	end

	local latex = string.format(
		[[
\begin{figure}
\centering
\includegraphics[keepaspectratio]{%s}
\caption[%s]{%s}%s
\end{figure}]],
		img.src,
		short,
		long_caption,
		label
	)

	return pandoc.RawBlock("latex", latex)
end
