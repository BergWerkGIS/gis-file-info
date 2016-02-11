SELECT 
    zoom_level
    , tile_column
    , tile_row
    , length(tile_data) as size
FROM tiles
WHERE
    size > 500 * 1024
ORDER BY
    size DESC
