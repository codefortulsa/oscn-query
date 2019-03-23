import oscn

# carter-CM-2019-14 has three cmid references

def test_string_params():
    county = 'tulsa'
    type = 'CM'
    year = '2018'

    list1 = oscn.request.CaseList(  types=type, counties=county,
                                years=year, start=21, stop=25)

    assert list1
    list1_indexes = []
    for case in list1:
        list1_indexes.append(case.index)
        assert case.county == county
        assert case.type == type
        assert case.year == year

    assert len(list1_indexes) == 5



def test_list_params():
    types=['CM','CF']
    counties=['oklahoma','tulsa']
    years=['2018', '2019']

    list1 = oscn.request.CaseList(  types=types, counties=counties,
                                    years=years, start=21, stop=25)
    assert list1

    list1_indexes = []
    for case in list1:
        list1_indexes.append(case.index)
        assert case.county in counties
        assert case.type in types
        assert case.year in years

    assert len(list1_indexes) == 40


def test_retrieve_cmids():
    # saving a list of cases should be retrievable by the same indexes
    list1 = oscn.request.CaseList(  types='CM', counties='carter',
                                years='2019', start=13, stop=16)

    list1_indexes = []
    for case in list1:
        list1_indexes.append(case.index)
        case.save(directory='data')

    assert len(list1_indexes) == 7


    list2_indexes = []
    for idx in list1_indexes:
        filed_case = oscn.request.Case(idx,directory='data')
        assert filed_case.valid
        filed_case.save(bucket='oscn-test-data')
        list2_indexes.append(filed_case.index)

    for idx in list2_indexes:
        bucket_case = oscn.request.Case(idx, bucket='oscn-test-data')
        assert bucket_case.valid


def test_retrieve_parent_and_cmids():
    parent_case_index ='johnston-CF-2011-00015'

    parent_case = oscn.request.Case(parent_case_index)
    assert parent_case.cmids
    assert len(parent_case.cmids) == 4

    list1 = oscn.request.CaseList(  counties='johnston', types='CF',
                                    years='2011', start=15, stop=15)


    for case in list1:

        assert case.county == parent_case.county
        assert case.year == parent_case.year

        get_case = oscn.request.Case(case.index)
        assert case.text == get_case.text