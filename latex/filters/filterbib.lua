-- write_bib.lua
local refs = {}

function Cite(el)
  for _, c in ipairs(el.citations) do
    refs[c.id] = true
  end
end

function Meta(meta)
  -- Grab bibliography files from metadata
  if meta.bibliography then
    local bibfiles = pandoc.utils.stringify(meta.bibliography)
    if type(bibfiles) == "string" then
      bibfiles = { bibfiles }
    end

    -- Process each .bib file
    for _, bibfile in ipairs(bibfiles) do
      local infile = io.open(bibfile, "r")
      local content = infile:read("*all")
      infile:close()

      local outfile = io.open("filtered.bib", "w")
      for entry in content:gmatch("@%w+%s*{.-\n}\n") do
        local key = entry:match("{%s*([^,]+),")
        if refs[key] then
          outfile:write(entry .. "\n")
        end
      end
      outfile:close()
    end
  end
end

