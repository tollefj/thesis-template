local box_styles = {
	bluebox = {
		colback = "blue!10!white",
		colframe = "blue!20!white",
		coltitle = "black",
	},
	yellowbox = {
		colback = "orange!10!white",
		colframe = "orange!20!white",
		coltitle = "black",
	},
	redbox = {
		colback = "red!10!white",
		colframe = "red!20!white",
		coltitle = "black",
	},
	greenbox = {
		colback = "green!10!white",
		colframe = "green!20!white",
		coltitle = "black",
	},
	graybox = {
		colback = "gray!10!white",
		colframe = "gray!20!white",
		coltitle = "black",
	},
	blackbox = {
		colback = "white",
		colframe = "black",
		coltitle = "white",
	},
}

function DivSimple(el)
	-- Default border thickness
	local default_boxrule = "0.5mm"

	for _, class_name in ipairs(el.classes) do
		if box_styles[class_name] then
			local style = box_styles[class_name]
			local title = el.attributes.title or ""
			local tex_pre = string.format(
				"\\begin{tcolorbox}[colback=%s, colframe=%s, coltitle=%s, title=\\textbf{%s}, boxrule=%s, width=\\textwidth]",
				style.colback,
				style.colframe,
				style.coltitle,
				title,
				default_boxrule
			)
			local new_content = { pandoc.RawBlock("latex", tex_pre) }
			for _, block in ipairs(el.content) do
				table.insert(new_content, block)
			end
			table.insert(new_content, pandoc.RawBlock("latex", "\\end{tcolorbox}"))
			return new_content
		end
	end
end

function Div(el)
	-- Border styling
	local default_boxrule = "0.5mm" -- overall border thickness
	local default_leftrule = nil -- individual side thickness (overrides boxrule)
	local default_rightrule = nil
	local default_toprule = nil
	local default_bottomrule = nil
	local default_arc = "3mm" -- corner roundness (0mm = sharp)

	-- Spacing
	local default_boxsep = "1mm" -- space between border and content
	local default_left = "5mm" -- internal margins
	local default_right = "5mm"
	local default_top = "3mm"
	local default_bottom = "3mm"

	-- Title styling
	local default_toptitle = "1mm" -- space above title text
	local default_bottomtitle = "1mm" -- space below title text
	local default_titlerule = "0.5mm" -- line between title and content (0mm = none)

	for _, class_name in ipairs(el.classes) do
		if box_styles[class_name] then
			local style = box_styles[class_name]
			local title = el.attributes.title or ""

			local options = string.format(
				"colback=%s, colframe=%s, coltitle=%s, title=\\textbf{%s}, boxrule=%s, arc=%s, boxsep=%s, left=%s, right=%s, top=%s, bottom=%s, toptitle=%s, bottomtitle=%s, titlerule=%s, width=\\textwidth",
				style.colback,
				style.colframe,
				style.coltitle,
				title,
				default_boxrule,
				default_arc,
				default_boxsep,
				default_left,
				default_right,
				default_top,
				default_bottom,
				default_toptitle,
				default_bottomtitle,
				default_titlerule
			)

			-- Add individual border rules if specified
			if default_leftrule then
				options = options .. string.format(", leftrule=%s", default_leftrule)
			end
			if default_rightrule then
				options = options .. string.format(", rightrule=%s", default_rightrule)
			end
			if default_toprule then
				options = options .. string.format(", toprule=%s", default_toprule)
			end
			if default_bottomrule then
				options = options .. string.format(", bottomrule=%s", default_bottomrule)
			end

			local tex_pre = string.format("\\begin{tcolorbox}[%s]", options)
			local new_content = { pandoc.RawBlock("latex", tex_pre) }
			for _, block in ipairs(el.content) do
				table.insert(new_content, block)
			end
			table.insert(new_content, pandoc.RawBlock("latex", "\\end{tcolorbox}"))
			return new_content
		end
	end
end
