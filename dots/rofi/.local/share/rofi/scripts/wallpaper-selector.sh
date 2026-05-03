#!/usr/bin/env bash

WALLPAPER_DIR="${WALLPAPER_DIR:-$HOME/.local/share/wallpapers}"
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/wallpaper-selector"
RASI_FILE="$HOME/.config/rofi/wallpaper-selector.rasi"

THUMB_SIZE=50

if [[ ! -d "$WALLPAPER_DIR" ]]; then
    notify-send "Wallpaper Selector" "Directory not found: $WALLPAPER_DIR" 2>/dev/null
    echo "Error: WALLPAPER_DIR '$WALLPAPER_DIR' does not exist." >&2
    exit 1
fi

mkdir -p "$CACHE_DIR"

generate_thumbnail() {
    local src="$1"
    # Use a hash of the full path as the cache key
    local hash
    hash=$(printf '%s' "$src" | md5sum | cut -d' ' -f1)
    local thumb="$CACHE_DIR/${hash}.png"

    if [[ ! -f "$thumb" ]]; then
        convert "$src" \
            -thumbnail "${THUMB_SIZE}x${THUMB_SIZE}^" \
            -gravity Center \
            -extent "${THUMB_SIZE}x${THUMB_SIZE}" \
            "$thumb" 2>/dev/null
    fi

    echo "$thumb"
}

shopt -s nullglob nocaseglob
IMAGE_FILES=("$WALLPAPER_DIR"/*.{jpg,jpeg,png,webp,bmp,gif,tiff})
shopt -u nullglob nocaseglob

if [[ ${#IMAGE_FILES[@]} -gt 1 ]]; then
    IFS=$'\n' IMAGE_FILES=( $(printf '%s\n' "${IMAGE_FILES[@]}" | sort -f) )
    unset IFS
fi

if [[ ${#IMAGE_FILES[@]} -eq 0 ]]; then
    notify-send "Wallpaper Selector" "No images found in $WALLPAPER_DIR" 2>/dev/null
    echo "No images found in '$WALLPAPER_DIR'." >&2
    exit 1
fi

build_input() {
    for img in "${IMAGE_FILES[@]}"; do
        local thumb
        thumb=$(generate_thumbnail "$img")
        [[ -z "$thumb" ]] && continue
        printf " \0icon\x1f%s\n" "$thumb"
    done
}

SELECTED=$(build_input | \
    rofi -dmenu \
         -show-icons \
         -theme "$RASI_FILE" \
         -p "" \
         -selected-row 0 \
         -format i)

[[ -z "$SELECTED" || ! "$SELECTED" =~ ^[0-9]+$ ]] && exit 0

CHOSEN_IMG="${IMAGE_FILES[$SELECTED]}"

if [[ -z "$CHOSEN_IMG" || ! -f "$CHOSEN_IMG" ]]; then
    notify-send "Wallpaper Selector" "Could not resolve selected image." 2>/dev/null
    exit 1
fi

qtile cmd-obj -o cmd -f fire_user_hook -a "set_wallpaper" "$(basename "$CHOSEN_IMG")"