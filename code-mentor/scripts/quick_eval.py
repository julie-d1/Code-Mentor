# src/eval/quick_eval.py
from codementor.mentor_agent import CodeMentor, MentorConfig

cases = [
    {
        "name": "Recursion confusion",
        "code": "def factorial(n):\n    return 1 if n==0 else n*factorial(n-1)",
        "msg": "I still don't get recursion 😫",
        "mode": "explain",
    },
    {
        "name": "Two-sum bug",
        "code": "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(len(nums)):\n            if nums[i]+nums[j]==target:\n                return i,j",
        "msg": "It sometimes returns the same index twice",
        "mode": "fix",
    },
    {
        "name": "Optimization hint",
        "code": "def is_prime(n):\n    for i in range(2,n):\n        if n%i==0: return False\n    return True",
        "msg": "Got it working! Any optimization tips?",
        "mode": "hint",
    },
]

mentor = CodeMentor(MentorConfig())
print("name, sentiment, bucket, level, complexity")
for c in cases:
    out = mentor.respond(c["code"], c["msg"], mode=c["mode"])
    print(f"{c['name']}, {out['sentiment']}, {out['skill_bucket']}, {out['skill_level']:.2f}, {out['complexity']}")
