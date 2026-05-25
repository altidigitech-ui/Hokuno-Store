#!/usr/bin/env bash
# Auto-generated rename+republish script for 125 old-format products
# Usage: nohup bash /workspaces/Hokuno-Store/rename_old.sh &
# Resumable: tracks done in /workspaces/Hokuno-Store/rename_done.txt

TOKEN="${PRINTIFY_API_TOKEN}"
SHOP_ID="22774508"
DONE="/workspaces/Hokuno-Store/rename_done.txt"
LOG="/workspaces/Hokuno-Store/rename.log"
touch "$DONE"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

rename_and_publish() {
  local ID="$1" TITLE="$2"
  
  if grep -qxF "$ID" "$DONE"; then log "[SKIP] $TITLE"; return; fi
  
  local retries=0
  while true; do
    HTTP=$(curl -s -o /dev/null -w "%{http_code}" -X PUT \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -H "User-Agent: ClaudeCode-Hokuno/1.0" \
      -d "{\"title\":\"$TITLE\"}" \
      "https://api.printify.com/v1/shops/$SHOP_ID/products/${ID}.json")
    if [ "$HTTP" = "200" ]; then break
    elif [ "$HTTP" = "429" ]; then retries=$((retries+1)); log "[429] pause 300s retry $retries — $TITLE"; sleep 300
    else log "[FAIL rename] HTTP $HTTP — $TITLE"; return; fi
  done
  
  retries=0
  while true; do
    HTTP=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -H "User-Agent: ClaudeCode-Hokuno/1.0" \
      -d '{"title":true,"description":false,"images":false,"variants":false,"tags":false,"keyFeatures":false,"shipping_template":false}' \
      "https://api.printify.com/v1/shops/$SHOP_ID/products/${ID}/publish.json")
    if [ "$HTTP" = "200" ] || [ "$HTTP" = "204" ]; then
      echo "$ID" >> "$DONE"
      log "[OK] $TITLE"
      break
    elif [ "$HTTP" = "429" ]; then retries=$((retries+1)); log "[429] publish pause 300s retry $retries — $TITLE"; sleep 300
    else log "[FAIL publish] HTTP $HTTP — $TITLE"; break; fi
  done
  
  sleep 2
}

rename_and_publish "69f630759110dda91005f3c6" "Bartolomiou Kouma • Wanted Poster Tee"
rename_and_publish "69f603f5ef66d02ffe02b1ce" "Lufi • Wanted Poster Black Tee"
rename_and_publish "69f6032239e419a2dc02e247" "Lufi • Wanted Poster Tee"
rename_and_publish "69f5ed40348775ebe705b79f" "Marshal Di Tittch • Wanted Poster Black Tee"
rename_and_publish "69f5ed3adb88631ee309c14d" "Marshal Di Tittch • Wanted Poster Tee"
rename_and_publish "69f5ed13e1b7b9b0b0086c22" "Alabastards • Wanted Poster Black Tee"
rename_and_publish "69f5ed0d348775ebe705b78d" "Alabastards • Wanted Poster Tee"
rename_and_publish "69f5ed06348775ebe705b78a" "Sharlot Linline • Wanted Poster Black Tee"
rename_and_publish "69f5ed00e1b7b9b0b0086c1b" "Sharlot Linline • Wanted Poster Tee"
rename_and_publish "69f5ecd14369722b330efb0e" "Doflamyngo • Wanted Poster Black Tee"
rename_and_publish "69f5eccb758757bfa304124d" "Doflamyngo • Wanted Poster Tee"
rename_and_publish "69f5ecc5ef66d02ffe02a1dc" "Caido • Wanted Poster Black Tee"
rename_and_publish "69f5ecbf758757bfa304124b" "Caido • Wanted Poster Tee"
rename_and_publish "69f5ecb9ef66d02ffe02a1db" "Baggy • Wanted Poster Black Tee"
rename_and_publish "69f5ecb3758757bfa3041249" "Baggy • Wanted Poster Tee"
rename_and_publish "69f5ecacecefd0d57d047d56" "Gymbey • Wanted Poster Black Tee"
rename_and_publish "69f5eca5ef66d02ffe02a1d2" "Gymbey • Wanted Poster Tee"
rename_and_publish "69f5ec9fe1b7b9b0b0086bfc" "God Ussop • Wanted Poster Black Tee"
rename_and_publish "69f5ec9a1cc4ed38fb0b7851" "God Ussop • Wanted Poster Tee"
rename_and_publish "69f5ec94cf535c302f083d3b" "Broock • Wanted Poster Black Tee"
rename_and_publish "69f5ec8b758757bfa3041238" "Broock • Wanted Poster Tee"
rename_and_publish "69f5ec84db88631ee309c111" "Francky • Wanted Poster Black Tee"
rename_and_publish "69f5ec7bcf535c302f083d29" "Francky • Wanted Poster Tee"
rename_and_publish "69f5ec75cf535c302f083d21" "Niko Robine • Wanted Poster Black Tee"
rename_and_publish "69f5ec68ecefd0d57d047d32" "Niko Robine • Wanted Poster Tee"
rename_and_publish "69f5ec5f1cc4ed38fb0b781b" "Shoper • Wanted Poster Black Tee"
rename_and_publish "69f5ec57ef66d02ffe02a19b" "Shoper • Wanted Poster Tee"
rename_and_publish "69f5ec51db88631ee309c0e4" "Sandji • Wanted Poster Black Tee"
rename_and_publish "69f5ec4b1cc4ed38fb0b77fc" "Sandji • Wanted Poster Tee"
rename_and_publish "69f5ec44db88631ee309c0b2" "Namy • Wanted Poster Black Tee"
rename_and_publish "69f5ec3fe1b7b9b0b0086b7e" "Namy • Wanted Poster Tee"
rename_and_publish "69f5ec391cc4ed38fb0b77d1" "Rororoa Zoro • Wanted Poster Black Tee"
rename_and_publish "69f5ec2fcf535c302f083ccd" "Rororoa Zoro • Wanted Poster Tee"
rename_and_publish "69f5ec26e1b7b9b0b0086b6e" "Chanks • Wanted Poster Black Tee"
rename_and_publish "69f5ec1fe1b7b9b0b0086b67" "Chanks • Wanted Poster Tee"
rename_and_publish "684eda3e09bce0c2370d8a5d" "Baggy • Wanted Poster Mug"
rename_and_publish "684ed9831d7c908d840ce998" "Caido • Wanted Poster Mug"
rename_and_publish "684ed8bad504d7af62062375" "Chanks • Wanted Poster Mug"
rename_and_publish "684ed81609bce0c2370d89f1" "Doflamyngo • Wanted Poster Mug"
rename_and_publish "684ed7650944c2e20d0f4c2f" "Francky • Wanted Poster Mug"
rename_and_publish "684ed66f09bce0c2370d899e" "God Ussop • Wanted Poster Mug"
rename_and_publish "684ed563b41682e82d0bcd1d" "Gymbey • Wanted Poster Mug"
rename_and_publish "684ed552047ae76743047c2d" "Tittch • Wanted Poster Mug"
rename_and_publish "684ed4c5047ae76743047c14" "Namy • Wanted Poster Mug"
rename_and_publish "684ed400b41682e82d0bcceb" "Niko Robine • Wanted Poster Mug"
rename_and_publish "684ed2d0d504d7af6206223c" "Zoro • Wanted Poster Mug"
rename_and_publish "684ed212047ae76743047b84" "Sandji • Wanted Poster Mug"
rename_and_publish "684ecfa38a7f6f02b7056fe0" "Sharlot Linline • Wanted Poster Mug"
rename_and_publish "684ecee209bce0c2370d881a" "Shoper • Wanted Poster Mug"
rename_and_publish "684ecdff047ae76743047ab5" "Broock • Wanted Poster Mug"
rename_and_publish "684eb0d009bce0c2370d8203" "Lufi • Wanted Poster Mug"
rename_and_publish "684dc28bb2d4e68c870e3445" "Alabastards • Wanted Poster Mug"
rename_and_publish "684d613ffef859492303a65a" "Zoro • Mythologie Case"
rename_and_publish "684d59ac1d7c908d840c9497" "Luffy • Mythologie Mug"
rename_and_publish "684c6b98f3b91cf7810bf40a" "Jinbe • Direction Black Tee"
rename_and_publish "684c6b5587f5fc4a810113bf" "Brook • Direction Black Tee"
rename_and_publish "684c6b157a567575d002f416" "Robin • Direction Black Tee"
rename_and_publish "684c6ac6f3b91cf7810bf3c6" "Franky • Direction Black Tee"
rename_and_publish "684c6a84b41682e82d0b43ac" "Choper • Direction Black Tee"
rename_and_publish "684c6a3fb41682e82d0b4390" "Ussop • Direction Black Tee"
rename_and_publish "684c69f1586f185e4005b09f" "Sanji • Direction Black Tee"
rename_and_publish "684c699f902f42fe2e080880" "Nami • Direction Black Tee"
rename_and_publish "684c693fb2d4e68c870de492" "Zoro • Direction Black Tee"
rename_and_publish "684c68d987f5fc4a8101133d" "Luffy • Direction Black Tee"
rename_and_publish "684c664a7a567575d002f304" "Jinbe • Direction Tee"
rename_and_publish "684c65fbdb8b74bc2d0b88bd" "Brook • Direction Tee"
rename_and_publish "684c65b97a567575d002f2d6" "Robin • Direction Tee"
rename_and_publish "684c656856fb86136206591f" "Franky • Direction Tee"
rename_and_publish "684c65141d7c908d840c5e16" "Choper • Direction Tee"
rename_and_publish "684c64cdf8df6e09820d1487" "Sanji • Direction Tee"
rename_and_publish "684c648061f0867d160dcdbb" "Ussop • Direction Tee"
rename_and_publish "684c64317a567575d002f25a" "Nami • Direction Tee"
rename_and_publish "684c63e57a567575d002f24c" "Zoro • Direction Tee"
rename_and_publish "684c63107a567575d002f21b" "Luffy • Direction Tee"
rename_and_publish "684b5414b0ad75db150b812b" "Alabastards • Wanted Poster Black Tee"
rename_and_publish "684b53a2a9314bdcdf0d5a62" "Baggy • Wanted Poster Black Tee"
rename_and_publish "684b532f90d6792b870aa071" "Caido • Wanted Poster Black Tee"
rename_and_publish "684b52a24a52709620072dec" "Chanks • Wanted Poster Black Tee"
rename_and_publish "684b520eff145207d8018ff7" "Doflamyngo • Wanted Poster Black Tee"
rename_and_publish "684b515f5ea5d8765401f813" "Francky • Wanted Poster Black Tee"
rename_and_publish "684b50d6c1b6866d8600de29" "God Ussop • Wanted Poster Black Tee"
rename_and_publish "684b50508ad27b8d90055731" "Gymbey • Wanted Poster Black Tee"
rename_and_publish "684b4fc190d6792b870a9fae" "Marshal Di Tittch • Wanted Poster Black Tee"
rename_and_publish "684b4f338ad27b8d900556ff" "Namy • Wanted Poster Black Tee"
rename_and_publish "684b4ead8b6650a870003f9e" "Niko Robine • Wanted Poster Black Tee"
rename_and_publish "684b4e188ad27b8d900556b7" "Rororoa Zoro • Wanted Poster Black Tee"
rename_and_publish "684b4d774a52709620072c94" "Sandji • Wanted Poster Black Tee"
rename_and_publish "684b4c7eea64cf1036087f88" "Sharlot Linline • Wanted Poster Black Tee"
rename_and_publish "684b4b9d8ad27b8d9005563e" "Shoper • Wanted Poster Black Tee"
rename_and_publish "684b44995ea5d8765401f580" "Broock • Wanted Poster Black Tee"
rename_and_publish "684b42ddc1b6866d8600db8f" "Lufi • Wanted Poster Black Tee"
rename_and_publish "684b40a48ad27b8d90055440" "Alabastards • Wanted Poster Tee"
rename_and_publish "684b3fee2c4daa76ec095919" "Baggy • Wanted Poster Tee"
rename_and_publish "684b3a018b6650a870003b88" "Caido • Wanted Poster Tee"
rename_and_publish "684b39093a95f8f9ac0cd9d7" "Chanks • Wanted Poster Tee"
rename_and_publish "684b37628ad27b8d900551ef" "Doflamyngo • Wanted Poster Tee"
rename_and_publish "684b35628ad27b8d90055159" "Francky • Wanted Poster Tee"
rename_and_publish "684b33afa9314bdcdf0d53d7" "God Ussop • Wanted Poster Tee"
rename_and_publish "684b327cb0ad75db150b79d1" "Gymbey • Wanted Poster Tee"
rename_and_publish "684b3118ff145207d801891c" "Marshal Di Tittch • Wanted Poster Tee"
rename_and_publish "684b300c4dfca61d6e03f94c" "Namy • Wanted Poster Tee"
rename_and_publish "684b2ef790d6792b870a98b8" "Niko Robine • Wanted Poster Tee"
rename_and_publish "684b2dfacd0c3157940915f8" "Rororoa Zoro • Wanted Poster Tee"
rename_and_publish "684b2d165ea5d8765401f04f" "Sandji • Wanted Poster Tee"
rename_and_publish "684b2b09a9314bdcdf0d5220" "Sharlot Linline • Wanted Poster Tee"
rename_and_publish "6849f9d953576a8a950e2eee" "Shoper • Wanted Poster Tee"
rename_and_publish "6849f7fc8b94b5b93d0fcd10" "Broock • Wanted Poster Tee"
rename_and_publish "6849d4756ab7f1ef5d06a2e9" "Lufi • Wanted Poster Tee"
rename_and_publish "6849c298b5bde8e15300e417" "Ussop • Mythologie Black Tee"
rename_and_publish "6849c1ce6ab7f1ef5d069e35" "Zoro • Mythologie Black Tee"
rename_and_publish "6849c0fc9bf7aebaf704867b" "Jinbe • Mythologie Black Tee"
rename_and_publish "6849c07b943f652c190bd88d" "Nami • Mythologie Black Tee"
rename_and_publish "6849bfd6943f652c190bd86d" "Franky • Mythologie Black Tee"
rename_and_publish "6849be2de27810926a088d94" "Sanji • Mythologie Black Tee"
rename_and_publish "6849b61fd0482255940866ea" "Luffy • Mythologie Black Tee"
rename_and_publish "6849a898e27810926a088854" "Ussop • Mythologie Tee"
rename_and_publish "6849a8397483e9399e0d455d" "Robin • Mythologie Black Tee"
rename_and_publish "6849a7abf43bb403450bd907" "Brook • Mythologie Tee"
rename_and_publish "6849a7517483e9399e0d44ef" "Choper • Mythologie Black Tee"
rename_and_publish "6849a6e0bd30bb1f1304c67e" "Sanji • Mythologie Tee"
rename_and_publish "6849a62c7483e9399e0d44b5" "Franky • Mythologie Tee"
rename_and_publish "6849a4e7d5b83610460568ba" "Jinbe • Mythologie Tee"
rename_and_publish "6849a4237483e9399e0d4444" "Nami • Mythologie Tee"
rename_and_publish "6849a0426ab7f1ef5d069673" "Zoro • Mythologie Tee"
rename_and_publish "6846b317f4071352350c150a" "Luffy • Mythologie Tee"

log "=== TERMINÉ === $(wc -l < /workspaces/Hokuno-Store/rename_done.txt) / 125 renommés"
