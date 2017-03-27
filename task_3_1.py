from html import escape as html_escape


__author__ = "Andrew Gafas"


def writer(mode):
    """
    Simple decorator that check incoming params and
    use relevant method's if exists.

    - mode - incoming param-modes (b,p,u,i)

    Returns a chain of applied methods

    """
    if not isinstance(mode, str):
        raise TypeError("Mode must be a characters (b,p,u,i,...)")

    def decorator(fn):
        func_list = {"p": tag_p, "b": tag_b, "u": tag_u, "i": tag_i}
        modes = list(mode)

        def wrapper(s):
            res = s
            for el in modes:
                if el in func_list.keys():
                    func = func_list[el]
                    res = func(res)

            return fn(res)

        return wrapper

    return decorator


def tag_p(s):
    new_s = "<p>{0}</p>".format(s)

    return new_s


def tag_b(s):
    new_s = "<b>{0}</b>".format(s)

    return new_s


def tag_i(s):
    new_s = "<i>{0}</i>".format(s)

    return new_s


def tag_u(s):
    new_s = "<u>{0}</u>".format(s)

    return new_s


@writer('bpx')
def html_printer(s):
    res_s = html_escape(s)

    return res_s


if __name__ == "__main__":
    print(html_printer("I'll give you +++ cash for this -> stuff."))
