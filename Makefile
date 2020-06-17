UNICODE_VERSION := 13.0.0
DOWNLOAD_URL_BASE := http://unicode.org/Public/$(UNICODE_VERSION)/ucd

DATA_FILES := $(addprefix unicode/, UnicodeData.txt CaseFolding.txt PropList.txt)
EAW_FILE   := unicode/EastAsianWidth.txt
EMOJI_FILE := unicode/emoji-data.txt
UNICODE_FILES := $(DATA_FILES) $(EAW_FILE) $(EMOJI_FILE)

all: UTF-8

UTF-8: $(UNICODE_FILES)
	python3 -B utf8_gen.py \
		-u unicode/UnicodeData.txt \
		-e unicode/EastAsianWidth.txt \
		-p unicode/PropList.txt \
		--unicode_version $(UNICODE_VERSION)

unicode:
	mkdir -p $@

$(DATA_FILES): | unicode
	curl --progress-bar -L -o $@ $(DOWNLOAD_URL_BASE)/$(notdir $@)

$(EAW_FILE): | unicode
	curl --progress-bar -L -o $@ $(DOWNLOAD_URL_BASE)/$(notdir $@) \
		&& patch -d unicode < EastAsianWidth.patch

$(EMOJI_FILE): | unicode
	curl --progress-bar -L -o $@ $(DOWNLOAD_URL_BASE)/emoji/$(notdir $@)

clean:
	$(RM) -r UTF-8 unicode

.PHONY: all clean
