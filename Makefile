UNICODE_VERSION := 13.0.0
DOWNLOAD_URL_BASE := http://unicode.org/Public/$(UNICODE_VERSION)/ucd

DATA_FILES := $(addprefix unicode/, UnicodeData.txt EastAsianWidth.txt PropList.txt)
EMOJI_FILE := unicode/emoji-data.txt
UNICODE_FILES := $(DATA_FILES) $(EMOJI_FILE)

GENERATED_EAW_FILE = EastAsianWidth.generated.txt

all: UTF-8 wcwidth9.h runewidth_table.go tables.rs

UTF-8: $(UNICODE_FILES) $(GENERATED_EAW_FILE)
	python3 -B utf8_gen.py \
		-u unicode/UnicodeData.txt \
		-e $(GENERATED_EAW_FILE) \
		-p unicode/PropList.txt \
		--unicode_version $(UNICODE_VERSION)

wcwidth9.h: $(UNICODE_FILES)
	ruby generate_wcwidth9.rb > $@

runewidth_table.go: $(UNICODE_FILES)
	ruby generate_runewidth_table.rb > $@

tables.rs: $(UNICODE_FILES)
	ruby generate_tables.rb > $@

unicode:
	mkdir -p $@

$(DATA_FILES): | unicode
	curl --progress-bar -L -o $@ $(DOWNLOAD_URL_BASE)/$(notdir $@)

$(EMOJI_FILE): | unicode
	curl --progress-bar -L -o $@ $(DOWNLOAD_URL_BASE)/emoji/$(notdir $@)

$(GENERATED_EAW_FILE): $(DATA_FILES)
	ruby generate_eaw.rb > $@

clean:
	$(RM) -r UTF-8 wcwidth9.h runewidth_table.go tables.rs unicode $(GENERATED_EAW_FILE)

.PHONY: all clean
