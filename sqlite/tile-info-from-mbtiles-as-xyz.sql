SELECT 
    zoom_level
    , tile_column as col
    , tile_row as row_tms
    --use binary shift to calculate xyz, as 'power' is not supported in sqlite by default
    , ((1 << zoom_level) - tile_row - 1) as row_xyz
    , length(tile_data) as size
FROM tiles
WHERE
    zoom_level = 11
