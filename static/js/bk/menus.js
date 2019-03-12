let menus_obj = {
    csrfToken: $("[name=csrfmiddlewaretoken]").val(),
    urlPageMenu: $('#url_page_menus').val(),
    urlAddMenu: $('#url_add_menu').val(),
    urlUpdateMenu: $('#url_update_menu').val(),
    urlObtainMenu: $('#url_obtain_menu').val(),

    titleRegex: new RegExp('\\S{2,64}'),
    urlRegex: new RegExp('\\S{4,200}'),
    modalAdd: $('#modal_add'),
    modalEdit: $('#modal_edit'),
    addInputTitle: $('#add_input_title'),
    addInputUrl: $('#add_input_url'),
    addInputSort: $('#add_input_sort'),
    addSelectIconClass: $('#add_select_icon_class'),
    addSelectParentMenu: $('#add_select_parent_menu'),
    addSelectIconClassSelect2: null,
    addSelectParentMenuSelect2: null,

    editInputTitle: $('#edit_input_title'),
    editInputUrl: $('#edit_input_url'),
    editInputSort: $('#edit_input_sort'),
    editSelectIconClass: $('#edit_select_icon_class'),
    editSelectParentMenu: $('#edit_select_parent_menu'),
    editSelectIconClassSelect2: null,
    editSelectParentMenuSelect2: null,
    editUserId: null,

    init: function () {
        $('#table_menus').DataTable({
            serverSide: true,
            processing: true,
            searching: true,
            autoWidth: false,
            language: {
                lengthMenu: 'Show _MENU_'
            },
            searchDelay: 2000,
            ajax: {
                url: menus_obj.urlPageMenu,
                type: 'POST',
                data: {'csrfmiddlewaretoken': menus_obj.csrfToken},
                dataFilter: function (resp) {
                    resp = $.parseJSON(resp);
                    if (resp.code === 10000) {
                        return JSON.stringify(resp.data);
                    }
                    return JSON.stringify({'error': resp.msg});
                }
            },
            createdRow: function (tr, data, dataIndex, tds) {
                $(tr).append('<td><button class="btn btn-primary btn-sm" onclick="menus_obj.show_edit_modal(' + data.id + ', this)">Edit Menu</button></td>')
            },
            columns: [
                {data: 'id'},
                {data: 'parent_id'},
                {data: 'title'},
                {data: 'url'},
                {data: 'icon_class', searchable: false},
                {
                    data: 'show',
                    createdCell: function (td, cellData, rowData, row, col) {
                        let style = cellData ? 'label-success' : 'label-default';
                        $(td).html('<lable class="label ' + style + '">' + cellData + '</lable>');
                    }
                },
                {data: 'sort', searchable: false},
                {data: 'update_time', searchable: false},
                {data: 'create_time', searchable: false},
                {
                    data: 'del_status',
                    searchable: false,
                    createdCell: function (td, cellData, rowData, row, col) {
                        let style = cellData ? 'label-danger' : 'label-info';
                        $(td).html('<lable class="label ' + style + '">' + cellData + '</lable>');
                    }
                }
            ],
        });
        let optionTemplate = function (state) {
            return $('<span<i class="fa ' + state.text + '"></i> ' + state.text + '</span>')
        };
        let iconClassSelect2Options = {
            placeholder: 'Select icon class',
            templateResult: optionTemplate,
            templateSelection: optionTemplate
        };
        menus_obj.addSelectIconClassSelect2 = menus_obj.addSelectIconClass.select2(iconClassSelect2Options);
        menus_obj.editSelectIconClassSelect2 = menus_obj.editSelectIconClass.select2(iconClassSelect2Options);

        let parentMenuSelect2Options = {
            placeholder: 'Select parent menu',
            delay: 300,
            cache: true,
            ajax: {
                url: menus_obj.urlPageMenu,
                method: 'POST',
                dataType: 'JSON',
                data: function (params) {
                    let start = (params.page ? params.page - 1 : 0) * 10;
                    let term = params.term ? params.term : '';
                    return {
                        start: start,
                        'columns[0][data]': 'title',
                        'columns[0][searchable]': 'true',
                        'columns[0][search][value]': term,
                        'columns[1][data]': 'show',
                        'columns[1][searchable]': 'true',
                        'columns[1][search][value]': '1',
                        csrfmiddlewaretoken: menus_obj.csrfToken
                    }
                },
                processResults: function (resp, params) {
                    if (resp.code === 10000) {
                        params.page = params.page || 1;
                        return {
                            "results": $.map(resp.data.data, function (menu) {
                                if (menu.id !== 1) {
                                    return {
                                        "id": menu.id,
                                        "text": menu.title
                                    }
                                }
                            }),
                            "pagination": {
                                "more": 10 * params.page < resp.data.recordsTotal
                            }
                        }
                    } else {
                        return null;
                    }
                }
            }
        };
        menus_obj.addSelectParentMenuSelect2 = menus_obj.addSelectParentMenu.select2(parentMenuSelect2Options);
        menus_obj.editSelectParentMenuSelect2 = menus_obj.editSelectParentMenu.select2(parentMenuSelect2Options);

        menus_obj.modalAdd.on('hidden.bs.modal', function (e) {
            menus_obj.add_clear();
        });

        menus_obj.modalEdit.on('hidden.bs.modal', function (e) {
            menus_obj.edit_clear();
        });
    },
    add_menu: function (btn) {
        let param = menus_obj.add_validate();
        if (param.is_submit) {
            $(btn).attr('disabled', 'disabled');
            $.ajax(menus_obj.urlAddMenu, {
                method: 'POST',
                dataType: 'JSON',
                data: {
                    csrfmiddlewaretoken: menus_obj.csrfToken,
                    title: param.title,
                    parent_id: param.parent_id,
                    url: param.url,
                    show: param.show,
                    icon_class: param.icon_class,
                    sort: param.sort,
                },
                success: function (resp) {
                    if (resp.code === 10000) {
                        menus_obj.modalAdd.modal('hide');
                        swal('Success', 'Menu add success', 'success').then(function () {
                            menus_obj.tableRoles.draw();
                        });
                    } else {
                        swal('Fail', 'Menu add fail: ' + resp.msg, 'error')
                    }
                },
                error: function (xhr, ts, et) {
                    swal('Fail', 'Menu add error: ' + et, 'error');
                },
                complete: function () {
                    $(btn).removeAttr('disabled');
                }
            });
        }
    },
    add_validate: function () {
        let is_submit = true;
        let title = menus_obj.addInputTitle.val();
        if (!menus_obj.titleRegex.test(title)) {
            menus_obj.addInputTitle.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let url = menus_obj.addInputUrl.val();
        if (url && !menus_obj.urlRegex.test(url)) {
            menus_obj.addInputUrl.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let parent_id = menus_obj.addSelectParentMenuSelect2.val();
        let show = menus_obj.modalAdd.find('input[name="show"]:checked').val();
        let iconClass = menus_obj.addSelectIconClassSelect2.val();
        let sort = menus_obj.addInputSort.val();
        return {
            is_submit: is_submit,
            parent_id: parent_id,
            title: title,
            url: url,
            show: show,
            sort: sort,
            icon_class: iconClass
        };
    },
    add_clear: function () {
        menus_obj.addInputUrl.val('');
        menus_obj.addInputTitle.val('');
        menus_obj.addInputSort.val('');
        menus_obj.modalAdd.find('input[name="show"][value="false"]').prop('checked', 'checked');
        menus_obj.addSelectIconClassSelect2.val(null).trigger('change');
        menus_obj.addSelectParentMenuSelect2.val(null).trigger('change');
    },
    show_edit_modal: function (id, btn) {
        //显示编辑菜单的modal
        $(btn).attr('disabled', 'disabled');
        menus_obj.editUserId = id;

        $.ajax(menus_obj.urlObtainMenu, {
            method: 'POST',
            dataType: 'JSON',
            data: {
                csrfmiddlewaretoken: menus_obj.csrfToken,
                id: id
            },
            success: function (resp) {
                if (resp.code === 10000) {
                    let menu = resp.data;
                    menus_obj.editInputTitle.val(menu.title);
                    menus_obj.editInputUrl.val(menu.url);
                    menus_obj.editInputSort.val(menu.sort);
                    if (menu.icon_class) {
                        menus_obj.editSelectIconClassSelect2.append(new Option(menu.icon_class, menu.icon_class, true, true));
                        menus_obj.editSelectIconClassSelect2.trigger('change');
                    }
                    if (meun_obj.parent_id) {
                        menus_obj.editSelectParentMenuSelect2.append(new Option(menu.parent_id, menu.parent_menu.title, true, true));
                        menus_obj.editSelectParentMenuSelect2.trigger('change');
                    }
                    menus_obj.modalEdit.find('input[name="show"][value="' + menu.show + '"]').prop('checked', true);
                    menus_obj.modalEdit.find('input[name="del_status"][value="' + menu.del_status + '"]').prop('checked', true);
                    menus_obj.modalEdit.modal('show');
                } else {
                    swal('Fail', 'Menu obtain fail: ' + resp.msg, 'error')
                }
            },
            error: function (xhr, ts, et) {
                swal('Fail', 'Menu obtain error: ' + et, 'error');
            },
            complete: function () {
                $(btn).removeAttr('disabled');
            }
        });
    },
    edit_menu: function (btn) {

    },
    edit_validate: function () {

    },
    edit_clear: function () {

    }
};
