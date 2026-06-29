## API

### NavigationLink

```swift
// NavigationLink隐藏右侧箭头
.navigationLinkIndicatorVisibility(.hidden)
```

### contentTransition

>   `contentTransition` 是 SwiftUI 里用来做**“同一个 view 内部内容变化”**的过渡动画，不是整页的 `transition`。它最适合文本数字、SF Symbols、颜色/大小变化这种内容更新场景

```swift
        Text("Welcome to SwiftUI! \(counter)")
            .font(.title)
            .foregroundStyle(
                .linearGradient(
                    colors: [.red, .green, .blue],
                    startPoint: .leading,
                    endPoint: .trailing
                )
            )
            .contentTransition(.numericText(value: Double(counter)))
            .onTapGesture {
                withAnimation {
                    counter += 1
                }
            }
```

### ButtonStyle 自定义按钮动画

>SwiftUI 里用来**统一定制按钮样式**的协议。你把很多按钮共用的外观、按下反馈、圆角、背景色这些逻辑集中写在一个 style 里，再用 `.buttonStyle(...)` 套到按钮上

```swift
struct ScaledButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration
            .label // configuration.label 是按钮内容
            .scaleEffect(configuration.isPressed ? 0.6 : 1) //能判断按钮是否正在被按下
            .animation(.interactiveSpring(), value: configuration.isPressed)
    }
}

// 使用
Button {}.buttonStyle(ScaledButtonStyle())
```

### rotationEffect 旋转动画

>   用来**旋转视图**的修饰符。它会让视图围绕指定锚点旋转，默认是中心点

```swift
@State private var isRotated = false
Button {
    isRotated.toggle()
} label: {
    Image(systemName: "chevron.right.circle")
        .font(.largeTitle)
        .rotationEffect(.degrees(isRotated ? 90 : 0))
        .animation(.default, value: isRotated)
}
```

### matchedGeometryEffect 平滑动画

>   做**两个视图之间平滑“连起来”动画**的修饰符

```swift
@Namespace var nameSpace
@State private var currentTab: Tab = .first

var body: some View {
ZStack {
    Color(uiColor: .secondarySystemBackground)
        .ignoresSafeArea()
    HStack(spacing: 0) {
        ForEach(Tab.allCases, id: \.self) { tab in
            Button {
                withAnimation {
                    currentTab = tab
                }
            } label: {
                Text(tab.rawValue)
                    .foregroundStyle(.black)
                    .padding(.vertical, 8)
                    .frame(maxWidth: .infinity)
                    .background {
                        if currentTab == tab {
                            Capsule()
                                .fill(.white)
                                .matchedGeometryEffect(
                                    id: "Tab",
                                    in: nameSpace
                                )
                        }
                    }
            }
        }
    }
    .frame(width: 200)
    .padding(2)
    .background {
        Capsule()
            .fill(.gray.opacity(0.5))
    }
}
}
```

### symbolEffect 系统图标动画

>   给 **SF Symbols** 加动画效果的修饰符

```swift
Button {
    isPulse.toggle()
} label: {
    Image(systemName: "arrowshape.up")
        .resizable()
        .scaledToFit()
        .imageScale(.large)
        .symbolEffect(.breathe, value: isPulse)
}

// .bounce .pulse .rotate .wiggle .variableColor

// .drawOn / .drawOff
```

### popoverTip 提示气泡

>   Apple **TipKit** 里的一个 SwiftUI 修饰符，用来把提示气泡挂在某个视图上，常见于功能引导、首次使用提示、按钮说明这类场景

```swift
struct PopoverTip: Tip {
    var title: Text {
        Text("查看详情")
            .foregroundStyle(.indigo)
    }
    
    var message: Text? {
        Text("点击 \(Image(systemName: "globe")) 查看更多信息")
    }
}

struct PopoverTipView: View {
    var body: some View {
        Text("Hello, world")
            .popoverTip(PopoverTip())
            .task {
                try? Tips.configure()
            }
    }
}
```

### keyframeAnimator 自定义的动画

>   做**分段、精确控制**动画的工具。它适合那种普通 `animation()` 不好表达的效果

```swift
struct PolishView: View {
    @State private var trigger = false
    var body: some View {
        Rectangle()
            .fill(Color.blue)
            .overlay {
                // 100 比较 hardcode 我们动态获取视图的高度
                GeometryReader { proxy in
                    let size = proxy.size
                    LinearGradient(
                        colors: [
                            Color.white.opacity(0),
                            Color.white.opacity(0),
                            Color.white.opacity(0),
                            Color.white.opacity(0.8),
                            Color.white.opacity(0),
                            Color.white.opacity(0),
                            Color.white.opacity(0),
                        ],
                        startPoint: .bottomLeading,
                        endPoint: .topTrailing
                    )
                    // 渐变视图左右两侧会出现露出缺角
                    // 我们放大 2 倍的 size, 避免出现这种情况
                    .scaleEffect(2)
                    .keyframeAnimator(
                        initialValue: 0,
                        trigger: trigger,
                        content: { content, progress in
                            // 我们需要将渐变色从 View 底部移动到 View 右上角
                            content
                                .offset(
                                    // 当 progress 从 0 到 1 的时候
                                    // offset 的 x 和 y 分别会趋近于 0
                                    // 偏移的距离还不够, 我们改为 2 倍
                                    x: -size.width + progress * size.width * 2,
                                    y: size.height - progress * size.height * 2
                                )
                        },
                        keyframes: { _ in
                            CubicKeyframe(0, duration: 0)
                            CubicKeyframe(1, duration: 1)
                        }
                    )
                }
            }
            .onTapGesture {
                trigger.toggle()
            }
            .frame(width: 200, height: 200)
            .cornerRadius(24)
    }
}
```

### navigationBarBackButtonHidden 隐藏按钮

>   **隐藏导航栏左上角返回按钮**的修饰符。它通常加在“被 push 进去的那个页面”上，而不是首页,**同时也会禁用侧滑返回手势**

```swift
// 这里要把它放在 DetailView 上，因为你想隐藏的是详情页的返回按钮
NavigationStack {
    NavigationLink("Detail") {
        DetailView()
            .navigationBarBackButtonHidden(true)
    }
}
```

### navigationTransition 导航跳转动画

>   iOS18+。定制**导航跳转动画**的修饰符。在 iOS 18 里常和 `.zoom` 一起用，做出类似 App Store 那种从卡片放大进入详情页的效果。它是给 `NavigationStack` / `NavigationLink` 的目的页设置过渡方式的

### matchedTransitionSource

>是 iOS 18+ 的 SwiftUI 修饰符，用来把某个视图标记成**导航转场的起点**，常见于 `.zoom` 这类 Hero 动画。它通常和 `navigationTransition(.zoom(sourceID:in:))` 配对使用

```swift
@Namespace private var namespace

NavigationStack {
    NavigationLink {
        DetailView()
            .navigationTransition(.zoom(sourceID: "item", in: namespace))
    } label: {
        Text("Item")
      //这里 id 和 namespace 要在源视图与目标视图之间一一对应
            .matchedTransitionSource(id: "item", in: namespace)
    }
}
```

## distortionEffect **几何扭曲**效果

>把每个像素的位置重新映射一下，而不是单纯改颜色
>
>通常和 **Metal shader库**一起用，如``ShaderLibrary.wave`

>   `ShaderLibrary.wave` 指的是 SwiftUI 里从 Metal shader 库中取出名为 `wave` 的着色器函数来用

>`maxSampleOffset` 是 `distortionEffect` 里的一个关键参数，用来告诉 SwiftUI：**这个变形最多会把像素往外挪多远**

```swift
Image("image-6")
    .distortionEffect(
        // 如果 time 是 1, 图片会出现固定的波纹效果
        ShaderLibrary.wave(.float(time)),

        maxSampleOffset: .zero
    )
```

**Metal shader库**

```metal
#include <metal_stdlib>
using namespace metal;

// 这里粘贴过来的方法是 SwiftUI 桥接 Shader 方法的固定写法
// 我们可以更改方法名称, 以及后面的额外参数
// 这里我添加了一个参数 time 用来做动态效果
[[ stitchable ]] float2 wave(float2 position, float time) {
    // position 为每隔像素点的位置
    // 我们将 y 得值动态增加 -1 ~ 1 (sin 之后的值)
    // 增加一些 y 的偏移幅度, 同时减少相邻 y 之间的差异 (position.y / 20, 之后会让 sin 0~1 的周期变长)
    position.y += 3 * sin(time + position.y / 20);
    return position;
}
```

## visualEffect 视觉效果

>用来给视图加“**视觉效果**”的修饰符，而且它会把该视图的布局信息一起提供给你用。它适合做缩放、偏移、模糊、透明度这类**不改变布局**、只改变视觉表现的效果

>简单来说，不改布局，只根据当前几何位置，给这个视图算出一个动态外观

## 帅气的图片转场例子

```swift
struct ImageTransitionAnimationView: View {
    @State private var toggle: Bool = false
    
    var body: some View {
        ZStack {
            if toggle {
                Image("car-image-1")
                    .resizable()
                    .transition(.blurReplace)
            } else {
                Image("car-image-2")
                    .resizable()
                    .transition(.blurReplace)
            }
        }
        .aspectRatio(contentMode: .fit)
        .frame(width: 300)
        .cornerRadius(24)
        .onTapGesture {
            withAnimation(.easeInOut(duration: 2)) {
                toggle.toggle()
            }
        }
    }
}
```



# 英文单词

| 单词                   | 意思                                 |
| :--------------------- | :----------------------------------- |
| abort                  | 中止、放弃、终止、终断               |
| usage                  | 用法、用途                           |
| command                | 命令、控制                           |
| circle                 | 圆、圆圈、圆形                       |
| capsule                | 胶囊形状                             |
| gradient               | 渐变                                 |
| radius                 | 半径                                 |
| stoke                  | 描边                                 |
| opactiy                | 不透明度                             |
| alignment              | 对齐                                 |
| infinity               | 无穷                                 |
| angle                  | 角度                                 |
| Resizable              | 自动调整大小                         |
| Fit \ fill             | 合适 \ 填满                          |
| clip                   | 剪裁                                 |
| foregroundStyle        | 前景色样式 (fore-前面、ground-面积） |
| overlay                | 覆盖、铺（例子：覆盖在圆形上面）     |
| renderingMode          | 渲染模式                             |
| scrollView             | 滚动视图                             |
| indices                | 返回集合范围索引的属性               |
| action                 | 执行                                 |
| Progress View          | 进度视图                             |
| Bool.toggle()          | 布尔值切换                           |
| Bool.description       | 返回字符串类型的布尔值               |
| ternary                | 三元                                 |
| Animation              | 动画特效                             |
| duration               | 持续时间                             |
| delay                  | 延迟                                 |
| transition             | 过渡动画                             |
| Animation.spring       | 弹簧特效                             |
| effect                 | 实现                                 |
| geometry               | 几何                                 |
| recent                 | 最近                                 |
| @Environment           | 环境                                 |
| slider                 | 滑动条                               |
| onAppear \ onDisappear | 出现时 \ 消失时                      |
| TopGesture             | 点击手势                             |
| AppStorage             | 数据储存                             |

# Xcode

|      说明       |        快捷键        |
| :-------------: | :------------------: |
| 折叠\展开 代码  | CTRL + ALT + ⬅️ or ➡️  |
| 调出系统图片等  |   CTRL + SHIFT + L   |
| 切换菜单栏Tab页 | CTRL + ⬅️ 或 CTRL + ➡️ |

1.   修改模拟器设备
     1.   菜单栏 -> Product -> Destination
2.   弹出表情:`CTRL + WIN + 空格`
3.   跳出系统自带图标`systemName`:`CTRL + SHIFT + L`

# 注解

|    注解名    | 含义                                                         |
| :----------: | :----------------------------------------------------------- |
|  **@State**  | 当状态值发生变化时，视图会自动刷新<br />只能用在 ==**struct**==,适合视图内部的私有状态 |
| **@Binding** | 双向数据绑定                                                 |
|    @Model    | SwiftData专属,作用在class上,持久化存储                       |
|              |                                                              |

# 代码笔记

## 字符串格式化

```swift
// 小数后面有很多值 只想要后面3位
var num = 514.6545446321

// 使用specifier,只能用于SwiftUI的 Text
Text("数字是 \(num, specifier: "%.3f")") // 输出:514.654

// String方法
String(format: "%.0f", age)
```

## 代码片段

```swift
Text("test")
	.id(1) // 给视图分配唯一标识符
	.lineLimit(1) // 用于限制文本只显示一行，超出部分会用省略号（…）表示。常用于 Text 或 TextField，防止内容换行。
	.minimumScaleFactor(0.1)
	.border(.red) // 加边框

Rectangle()
    .fill(Color(.systemBackground)) // 填充为系统颜色
```

## 百分号编码

|  字元  | 百分号编码 |
| :----: | ---------- |
| 空白键 | %20        |
|   =    | %3D        |
|   ?    | %3F        |
|   #    | %23        |
|   &    | %26        |

# 6.犯错点

1.   ForEach 是 SwiftUI 的视图构造器，主要用来生成 View，不支持插入数据。使用==for num in 0...10 {}==
