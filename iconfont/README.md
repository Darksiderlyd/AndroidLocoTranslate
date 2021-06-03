1.
进入ali iconfont 官网 https://www.iconfont.cn/?spm=a313x.7781069.1998910419.d4d0a486a
Resources -> MyProject -> Driven Projects -> 长桥 客户端
没有的可以让 @沉弘 加一下

2.Download Code下载download.zip放到toolsiconfont下

3.执行脚本
```
cd toolsiconfont
sh iconfontCreate.sh
```
4.自动添加iconfont.ttf、生成IconFont.java

5.使用
- 组件github链接 https://github.com/mikepenz/Android-Iconics/tree/v3.2.5
- 使用Drawable
new IconicsDrawable(this)
    .icon(FontAwesome.Icon.faw_android)
    .color(Color.RED)
    .sizeDp(24)

- ImageView
<com.mikepenz.iconics.view.IconicsImageView
      android:layout_width="72dp"
      android:layout_height="72dp"
      app:iiv_color="@android:color/holo_red_dark"
      app:iiv_icon="gmd-favorite" />  // or @string/gmd_favorite with our generator

- TextView
<com.mikepenz.iconics.view.IconicsTextView
        android:text="abc{hif-test}defgh{faw-adjust}ijk{fon-test1}lmnopqrstuv{fon-test2}wxyz"
        android:textColor="@android:color/black"
        android:layout_width="wrap_content"
        android:layout_height="56dp"
        android:textSize="16sp"/>

- IconicsButton
<com.mikepenz.iconics.view.IconicsButton
        android:text="{faw-adjust} Button"
        android:layout_width="120dp"
        android:layout_height="60dp"/>