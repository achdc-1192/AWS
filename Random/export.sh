grep AccessKeyId | cut -d ':' -f2 | sed 's/[^0-9A-Z]*//g'
grep SecretAccessKey | cut -d':' -f2 | sed 's/[^0-9A-Za-z/+=]*//g'`
