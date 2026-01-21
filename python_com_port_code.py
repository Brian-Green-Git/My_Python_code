# for (int t = 0; t < nums.size(); i++, t++)
# 		nums[t] = (i + 1.0) * y;

# 		for (double i : nums)
# 		{
# 			num.push_back((i * sqrt(x * y)) / exp(pow(i, 0.1)));

# 		}

# 		for (double i : num)
# 		{
# 			ans = (cos(ans + i)) / log(z + i);
# 		}
# 	

#%%
import math

num = [100]
nums = [100]
t = 1
x = 10.0
y = 2.0
z = 75.0
ans = 0.0

#%%
for i in num:
    num.append((t + 1.0) * y)
    
#%%

for i in nums:
    nums.append(((i * math.sqrt(x * y))/ math.exp(math.pow(i, 0.1))))

for i in nums:
    ans = (math.cos(ans + 1)/ math.log(z+i))
    
    
print(f"{ans =}")