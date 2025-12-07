-- Short captions for tables in LaTeX output
io.stderr:write("short-captions-table.lua is running\n")

if FORMAT ~= "latex" then
	return
end

function Table(tbl)
	local short = tbl.attributes["short-caption"]
	if not short then
		return nil
	end

	-- Modify the caption to include short caption
	if tbl.caption and tbl.caption.long then
		-- Create a new caption structure with short caption
		local long_inlines = tbl.caption.long
		local short_inlines = pandoc.Inlines(pandoc.Str(short))

		-- Update the caption with short form
		tbl.caption.short = short_inlines
	end

	return tbl
end
