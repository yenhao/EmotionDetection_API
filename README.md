# EmotionDetection_API

## Chinese Emotion Classifier
The api is build to handle the massive query, which using multi-processing to process the query message to classify the emotion.

ISSUE: With lots of query, the waiting time will be long. Due to the first in first out process.
d
The scale up version will build in the future.

## Query

Input : json object

```
  { data : [
    {
      "message": "抽顯卡做研究 DeepLearning + 黑色沙漠",
      ...
    },
    {
      "message": "送趙奕誠出國報conference",ds
      ...
    }...
    ]
  }
```

Output: json object
```
  { data : [
    {
      "message": "抽顯卡做研究 DeepLearning + 黑色沙漠",
      "emotion1": "anger",
      "emotion2": "haha",
      "ambiguous" "True"
    },
    {
      "message": "送趙奕誠出國報conference",
      "emotion1": "Sad",
      "emotion2": "anger",
      "ambiguous" "False"
    }...
    ]ss
  }
```
The example is in the [EmotionDetection_ch](EmotionDetection_ch.py)
