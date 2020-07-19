from ggit.cli import get_args


def main():
    args = vars(get_args())
    func = args.pop("func")
    func(**args)


if __name__ == "__main__":
    main()
