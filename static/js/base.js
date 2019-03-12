let meun_obj = {
    init: function (_opt) {
        let menus = JSON.parse(_opt.menus_json);
        let ul_menu = $('.sidebar-menu');
        menus.filter(function (menu) {
            return !menu.parent_id
        }).forEach(function (menu) {
            //parent_id is null
            if (!menu.url) {
                //url is '' 表示一级父菜单
                let content =
                    '<li id="li_' + menu.id + '" class="treeview">' +
                    '<a href="#">' +
                    '<i class="fa ' + menu.icon_class + '"></i>' +
                    '<span> ' + menu.title + '</span>' +
                    '<span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span>' +
                    '</a>' +
                    '<ul class="treeview-menu"> </ul>' +
                    '</li>';
                ul_menu.append(content);
            } else {
                //表示一级菜单
                let content = '<li id="li_' + menu.id + '" class="' + (_opt.session_select_url === menu.url ? 'active' : '') + '"><a href="' + menu.url + '"><i class="fa ' + menu.icon_class + '"></i> <span> ' + menu.title + '</span></a></li>';
                ul_menu.append(content);
            }
        });

        menus.filter(function (menu) {
            return menu.parent_id && !menu.url
        }).forEach(function (menu) {
            let li_menu = $('#li_' + menu.parent_id);
            //二级父菜单
            let content =
                '<li id="li_' + menu.id + '" class="treeview">' +
                '<a href="#">' +
                '<i class="fa ' + menu.icon_class + '"></i>' +
                '<span>' + menu.title + '</span>' +
                '<span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span>' +
                '</a>' +
                '<ul class="treeview-menu"> </ul>' +
                '</li>';
            li_menu.children('.treeview-menu').append(content);
        });

        menus.filter(function (menu) {
            return menu.parent_id && menu.url
        }).forEach(function (menu) {
            let li_menu = $('#li_' + menu.parent_id);
            li_menu.children('.treeview-menu').append('<li id="li_' + menu.id + '" class="' + (_opt.session_select_url === menu.url ? 'active' : '') + '"><a href="' + menu.url + '"><i class="fa ' + menu.icon_class + '"></i> ' + menu.title + '</a></li>')
            if (_opt.session_select_url === menu.url) {
                li_menu.addClass('active').parents('.treeview').addClass('active');
            }
        })
    }
};