import polib
import rich

from tqdm import tqdm
from googletranslatepy import Translator


def string_escape_wrapper(func):
    encode_i18n_var = lambda str: '{@'.join(str.split("{"))
    decode_i18n_var = lambda str: '{'.join(str.split("{@"))

    def wrapper(translator: Translator, msgid: str, msgstr: str):
        result = func(translator, encode_i18n_var(msgid), encode_i18n_var(msgstr))
        return decode_i18n_var(result)

    return wrapper


@string_escape_wrapper
def translate_entry(translator: Translator, msgid: str, msgstr: str):
    if len(msgstr) == 0:
        return translator.translate(msgid)
    if msgstr.startswith(' '):
        return f" {translator.translate(msgstr)}"
    else:
        return translator.translate(msgstr)


def translate_po(filepath_in: str, filepath_out: str, lang: str):
    translator = Translator(target=lang)
    po = polib.pofile(filepath_in)

    for entry in tqdm(po):
        entry.msgstr = translate_entry(translator, entry.msgid, entry.msgstr)

    po.metadata["Language"] = lang
    po.save(filepath_out)

    rich.print(f"\n[bold green]Translation finished successfully[/bold green] (saved in \"{filepath_out}\")")


def translate_mo(filepath_in: str, filepath_out: str, lang: str):
    translator = Translator(target=lang)
    po = polib.mofile(filepath_in)

    for entry in tqdm(po):
        entry.msgstr = translate_entry(translator, entry.msgid, entry.msgstr)

    po.metadata["Language"] = lang
    po.save(filepath_out)

    rich.print(f"\n[bold green]Translation finished successfully[/bold green] (saved in \"{filepath_out}\")")


def translate_po_to_mo(filepath_in: str, filepath_out: str, lang: str):
    translator = Translator(target=lang)
    po = polib.pofile(filepath_in)

    for entry in tqdm(po):
        entry.msgstr = translate_entry(translator, entry.msgid, entry.msgstr)

    po.metadata["Language"] = lang
    po.save_as_mofile(filepath_out)

    rich.print(f"\n[bold green]Translation finished successfully[/bold green] (saved in \"{filepath_out}\")")
