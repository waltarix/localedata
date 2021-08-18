UNICODE_VERSION   := 14.0.0
DOWNLOAD_URL_BASE := https://unicode.org/Public/$(UNICODE_VERSION)/ucd

DATA_FILES    := $(addprefix unicode/, UnicodeData.txt EastAsianWidth.txt PropList.txt)
EMOJI_FILE    := unicode/emoji-data.txt
UNICODE_FILES := $(DATA_FILES) $(EMOJI_FILE)

GLIBC_VERSION        := 2.34
UNICODE_GEN_URL_BASE := https://raw.githubusercontent.com/bminor/glibc/glibc-$(GLIBC_VERSION)/localedata/unicode-gen
UNICODE_GEN_FILES    := utf8_gen.py unicode_utils.py

GENERATED_EAW_FILE := EastAsianWidth.generated.txt

PYTHON := poetry run python
CURL   := curl --progress-bar -L

CACHE_FILES := $(addprefix .cache/, eaw.pickle wcwidth9.pickle)

all: UTF-8 wcwidth9.h runewidth_table.go tables.rs

UTF-8: $(UNICODE_FILES) $(GENERATED_EAW_FILE) $(UNICODE_GEN_FILES)
	$(PYTHON) -B utf8_gen.py \
		-u unicode/UnicodeData.txt \
		-e $(GENERATED_EAW_FILE) \
		-p unicode/PropList.txt \
		--unicode_version $(UNICODE_VERSION)

wcwidth9.h: $(UNICODE_FILES) $(CACHE_FILES)
	$(PYTHON) src/generate/wcwidth9_h > $@

runewidth_table.go: $(UNICODE_FILES) $(CACHE_FILES)
	$(PYTHON) src/generate/runewidth_table_go > $@

tables.rs: $(UNICODE_FILES) $(CACHE_FILES)
	$(PYTHON) src/generate/tables_rs > $@

unicode:
	mkdir -p $@

$(DATA_FILES): | unicode
	$(CURL) -o $@ $(DOWNLOAD_URL_BASE)/$(notdir $@)

$(EMOJI_FILE): | unicode
	$(CURL) -o $@ $(DOWNLOAD_URL_BASE)/emoji/$(notdir $@)

$(UNICODE_GEN_FILES):
	$(CURL) -o $@ $(UNICODE_GEN_URL_BASE)/$@

$(GENERATED_EAW_FILE): $(DATA_FILES) $(CACHE_FILES)
	$(PYTHON) src/generate/east_asian_width_txt > $@

$(CACHE_FILES) &: $(DATA_FILES)
	$(PYTHON) src/generate/util/cache

clean: mostlyclean
	$(RM) -r UTF-8 unicode $(UNICODE_GEN_FILES) $(CACHE_FILES)

mostlyclean:
	$(RM) -r wcwidth9.h runewidth_table.go tables.rs $(GENERATED_EAW_FILE)

.PHONY: all clean mostlyclean
