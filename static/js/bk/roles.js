let roles_obj = {
    csrfToken: $("[name=csrfmiddlewaretoken]").val(),
    urlPageRoles: $("#url_page_roles").val(),
    urlAllMenus: $("#url_all_menus").val(),
    urlAddRole: $('#url_add_role').val(),
    urlUpdateRole: $('#url_update_role').val(),
    urlObtainRole: $('#url_obtain_role').val(),

    nameRegex: new RegExp('[A-Z0-9_]{3,32}'),

    modalAdd: $('#modal_add'),
    modalEdit: $('#modal_edit'),
    addInputName: $("#add_input_name"),
    editInputName: $("#edit_input_name"),
    addMenuTree: $("#add_menu_tree"),
    editMenuTree: $("#edit_menu_tree"),

    tableRoles: null,
    editUserId: null,
    menuTreeSetting: {
        view: {
            showLine: false
        },
        check: {
            enable: true
        },
        data: {
            simpleData: {
                enable: true
            }
        },
        callback: {
            onClick: function (event, treeId, treeNode) {
                let zTree = $.fn.zTree.getZTreeObj("menu_tree");
                zTree.checkNode(treeNode, null, true, false);
            }
        }
    },

    init: function (_opt) {
        roles_obj.tableRoles = $('#table_roles').DataTable({
            serverSide: true,
            processing: true,
            searching: true,
            autoWidth: false,
            language: {
                lengthMenu: 'Show _MENU_'
            },
            searchDelay: 2000,
            ajax: {
                url: roles_obj.urlPageRoles,
                type: 'POST',
                data: {csrfmiddlewaretoken: roles_obj.csrfToken},
                dataFilter: function (resp) {
                    resp = $.parseJSON(resp);
                    if (resp.code === 10000) {
                        return JSON.stringify(resp.data);
                    }
                    return JSON.stringify({'error': resp.msg});
                },
                error: function (xhr, ts, et) {
                    swal('Fail', 'Obtain page role error: ' + et, 'error');
                }
            },
            createdRow: function (tr, data, dataIndex, tds) {
                $(tr).append('<td><button class="btn btn-primary btn-sm" onclick="roles_obj.show_edit_modal(' + data.id + ', this)">Edit Role</button></td>')
            },
            columns: [
                {data: 'id'},
                {data: 'name'},
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

        roles_obj.modalAdd.on('show.bs.modal', function (e) {
            //添加的模态框显示前去获取菜单列表
            $.ajax(roles_obj.urlAllMenus, {
                method: 'POST',
                dataType: 'JSON',
                data: {
                    csrfmiddlewaretoken: roles_obj.csrfToken
                },
                success: function (resp) {
                    if (resp.code === 10000) {
                        let nodes = $.map(resp.data.data, function (menu) {
                            return {
                                id: menu.id,
                                pId: menu.parent_id,
                                name: menu.title,
                                is_parent: !menu.parent_id || !menu.url,
                                open: true,
                                checked: menu.url === '/index/' || menu.url === '/backend/profile/'
                            }
                        });
                        $.fn.zTree.init(roles_obj.addMenuTree, roles_obj.menuTreeSetting, nodes);
                    } else {
                        swal('Fail', 'Obtain menus fail: ' + resp.msg, 'error')
                    }
                },
                error: function (xhr, ts, et) {
                    swal('Fail', 'Obtain menus error: ' + et, 'error');
                }
            });
        });

        roles_obj.modalAdd.on('hidden.bs.modal', function (e) {
            roles_obj.add_clear();
        });

        roles_obj.modalEdit.on('hidden.bs.modal', function (e) {
            roles_obj.edit_clear();
        });
    },
    add_role: function (btn) {
        let param = roles_obj.add_validate();
        if (param.is_submit) {
            $(btn).attr('disabled', 'disabled');
            $.ajax(roles_obj.urlAddRole, {
                method: 'POST',
                dataType: 'JSON',
                data: {
                    csrfmiddlewaretoken: roles_obj.csrfToken,
                    name: param.name,
                    menus: param.menus.join(',')
                },
                success: function (resp) {
                    if (resp.code === 10000) {
                        roles_obj.modalAdd.modal('hide');
                        swal('Success', 'Role add success', 'success').then(function () {
                            roles_obj.tableRoles.draw();
                        });
                    } else {
                        swal('Fail', 'Role add fail: ' + resp.msg, 'error')
                    }
                },
                error: function (xhr, ts, et) {
                    swal('Fail', 'Role add error: ' + et, 'error');
                },
                complete: function () {
                    $(btn).removeAttr('disabled');
                }
            });
        }
    },
    add_validate: function () {
        let is_submit = true;
        let name = roles_obj.addInputName.val();
        if (!roles_obj.nameRegex.test(name)) {
            roles_obj.addInputName.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let zTree = $.fn.zTree.getZTreeObj("add_menu_tree");
        let nodes = zTree.getCheckedNodes(true);
        if (nodes.length < 1) {
            roles_obj.addMenuTree.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        return {
            is_submit: is_submit,
            name: name,
            menus: $.map(nodes, function (node) {
                return node.id
            })
        };
    },
    add_clear: function () {
        roles_obj.addInputName.val('');
        roles_obj.modalAdd.find('.form-group').removeClass('has-error').removeClass('has-success')
            .find('span > i').removeClass('fa-times').removeClass('fa-check')
    },
    edit_validate: function () {
        let is_submit = true;
        let name = roles_obj.editInputName.val();
        if (!roles_obj.nameRegex.test(name)) {
            roles_obj.editInputName.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let zTree = $.fn.zTree.getZTreeObj("edit_menu_tree");
        let nodes = zTree.getCheckedNodes(true);
        if (nodes.length < 1) {
            roles_obj.addMenuTree.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let del_status = roles_obj.modalEdit.find('input[name="del_status"]:checked').val();
        return {
            is_submit: is_submit,
            name: name,
            del_status: del_status,
            menus: $.map(nodes, function (node) {
                return node.id
            })
        };
    },
    show_edit_modal: function (id, btn) {
        //显示编辑角色的modal
        $(btn).attr('disabled', 'disabled');
        roles_obj.editUserId = id;

        //先获取角色，然后获取所有菜单
        $.ajax(roles_obj.urlObtainRole, {
            method: 'POST',
            dataType: 'JSON',
            async: true,
            data: {
                csrfmiddlewaretoken: roles_obj.csrfToken,
                id: id
            },
            success: function (resp) {
                if (resp.code === 10000) {
                    roles_obj.editInputName.val(resp.data.name);
                    roles_obj.modalEdit.find('input[name="del_status"][value="' + resp.data.del_status + '"]').prop('checked', true);
                    let role_menus = $.map(resp.data.menus, function (menu) {
                        return menu.id
                    });

                    $.ajax(roles_obj.urlAllMenus, {
                        method: 'POST',
                        dataType: 'JSON',
                        async: true,
                        data: {
                            csrfmiddlewaretoken: roles_obj.csrfToken
                        },
                        success: function (menu_resp) {
                            if (menu_resp.code === 10000) {
                                let nodes = $.map(menu_resp.data, function (menu) {
                                    return {
                                        id: menu.id,
                                        pId: menu.parent_id,
                                        name: menu.title,
                                        is_parent: !menu.parent_id || !menu.url,
                                        open: true,
                                        checked: role_menus.indexOf(menu.id) >= 0
                                    }
                                });
                                $.fn.zTree.init(roles_obj.editMenuTree, roles_obj.menuTreeSetting, nodes);
                                roles_obj.modalEdit.modal('show');
                            } else {
                                swal('Fail', 'Obtain menus fail: ' + menu_resp.msg, 'error')
                            }
                        },
                        error: function (xhr, ts, et) {
                            swal('Fail', 'Obtain menus error: ' + et, 'error');
                        }
                    });
                } else {
                    swal('Fail', 'Role obtain fail: ' + resp.msg, 'error')
                }
            },
            error: function (xhr, ts, et) {
                swal('Fail', 'Role obtain error: ' + et, 'error');
            },
            complete: function () {
                $(btn).removeAttr('disabled');
            }
        });
    },
    edit_role: function (btn) {
        let param = roles_obj.edit_validate();
        if (param.is_submit) {
            $(btn).attr('disabled', 'disabled');
            $.ajax(roles_obj.urlUpdateRole, {
                method: 'POST',
                dataType: 'JSON',
                data: {
                    csrfmiddlewaretoken: roles_obj.csrfToken,
                    id: roles_obj.editMenuId,
                    name: param.name,
                    del_status: param.del_status,
                    menus: param.menus.join(',')
                },
                success: function (resp) {
                    if (resp.code === 10000) {
                        roles_obj.modalEdit.modal('hide');
                        swal('Success', 'Role update success', 'success').then(function () {
                            roles_obj.tableRoles.draw();
                        });
                    } else {
                        swal('Fail', 'Role update fail: ' + resp.msg, 'error')
                    }
                },
                error: function (xhr, ts, et) {
                    swal('Fail', 'Role update error: ' + et, 'error');
                },
                complete: function () {
                    $(btn).removeAttr('disabled');
                }
            });
        }
    },
    edit_clear: function () {
        //清空编辑模态框中的数据
        roles_obj.editInputName.val('');
        roles_obj.modalEdit.find('.form-group').removeClass('has-error').removeClass('has-success')
            .find('span > i').removeClass('fa-times').removeClass('fa-check');
        roles_obj.modalEdit.find('input[name="del_status"]').removeProp('checked');
    }
};