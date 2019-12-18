from engine.search_engine import parse_arguments
from engine.search_engine import get_site_data
from engine.search_engine import get_start_point_links_set
from engine.search_engine import print_inner_links


def main():
    args = parse_arguments()
    
    site_data = get_site_data(args.start_point, args.search_query, args.number)
    start_point_links = get_start_point_links_set(site_data, args.start_point)

    if int(args.recursion) > 0:
        print_inner_links(start_point_links)

    else:
        for link in start_point_links:
            print(link)


if __name__ == '__main__':
    main()
