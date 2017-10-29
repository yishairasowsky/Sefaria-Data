#encoding=utf-8

from sources.Shulchan_Arukh.ShulchanArukh import *

root = Root('Orach_Chaim.xml')
commentaries = root.get_commentaries()
taz = commentaries.get_commentary_by_title("Taz on Orach Chayim")
if taz is None:
    taz = commentaries.add_commentary("Taz on Orach Chayim", u"טז על אורח חיים")


filenames = [u"./txt_files/Orach_Chaim/part_1/שוע אורח חיים חלק א טז.txt",
             u"./txt_files/Orach_Chaim/part_2/שולחן ערוך אורח חיים חלק ב טז מגן דוד.txt",
             u"./txt_files/Orach_Chaim/part_3/שו''ע אורח חיים חלק ג -טז מושלם.txt"]
for i, filename in enumerate(filenames):
    taz.remove_volume(i+1)
    # correct_marks_in_file(filename, u'@00([\u05d0-\u05ea]{1,2})', u'@22([\u05d0-\u05ea]{1,3})')
    with codecs.open(filename, 'r', 'utf-8') as infile:
        volume = taz.add_volume(infile.read(), i+1)
    assert isinstance(volume, Volume)

    errors = volume.mark_simanim(u'@00([\u05d0-\u05ea]{1,3})') if i == 0 else volume.mark_simanim(u'@22([\u05d0-\u05ea]{1,3})')
    volume.validate_simanim(complete=False)

    errors += volume.mark_seifim(u'@22\(([\u05d0-\u05ea]{1,3})\)') if i == 0 else volume.mark_seifim(u'@11([\u05d0-\u05ea]{1,3})')
    volume.validate_seifim()

    errors += volume.format_text('@11', '@33', 'dh')


    base = root.get_base_text()
    base.add_titles("Orach Chaim", u"אורח חיים")
    b_vol = base.get_volume(1)
    try:
        b_vol.mark_references(volume.get_book_id(), u'@77\(([\u05d0-\u05ea]{1,3})\)', group=1)
    except AssertionError:
        pass
    assert isinstance(b_vol, Volume)
    volume.set_rid_on_seifim()
    errors += root.populate_comment_store()
    errors += b_vol.validate_all_xrefs_matched(lambda x: x.name == 'xref' and re.search(u'@77', x.text) is not None, base="Orach Chaim", commentary="Taz on Orach Chaim", simanim_only=True)
    for i in errors:
        print i

    root.export()
