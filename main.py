import parse_json as parse


def main():
    parse.get_parse_and_save(test_mode=False, add_sub_links=False)
    parse.print_summary()

# ToDo: Add command line argument to select test mode and sublink option
if __name__ == '__main__':
    main()
