// SPDX-License-Identifier: GPL-2.0
/*
 * Copyright (C) 2020 Mikhael Khrustik <misha@myrt.co>.
 *
 * CPU Input Boost:
 * Copyright (C) 2018-2019 Sultan Alsawaf <sultan@kerneltoast.com>.
 */

#include <linux/cpu.h>
#include <linux/cpufreq.h>
#include <linux/msm_drm_notify.h>

static bool screen_on = true;
static struct notifier_block cpu_notif;
static struct notifier_block msm_drm_notif;

static unsigned int get_min_freq(struct cpufreq_policy *policy)
{
	unsigned int freq;

	if (cpumask_test_cpu(policy->cpu, cpu_lp_mask))
		freq = CONFIG_FREQ_LIMIT_MIN_LP;
	else
		freq = CONFIG_FREQ_LIMIT_MIN_PERF;

	return max(freq, policy->min);
}

static unsigned int get_max_freq(struct cpufreq_policy *policy)
{
	unsigned int freq;

	if (cpumask_test_cpu(policy->cpu, cpu_lp_mask))
		freq = CONFIG_FREQ_LIMIT_MAX_LP;
	else
		freq = CONFIG_FREQ_LIMIT_MAX_PERF;

	if (freq)
		return freq;

	return policy->max;
}

static int cpu_notifier_cb(struct notifier_block *nb, unsigned long action,
			   void *data)
{
	struct cpufreq_policy *policy = data;
	int next_min;

	if (action != CPUFREQ_ADJUST)
		return NOTIFY_OK;
    
    	policy->max = get_max_freq(policy);

	if (screen_on) {
		next_min = get_min_freq(policy);
		if (policy->min < next_min) {
			policy->min = next_min;
		}
		return NOTIFY_OK;
	} 

	/* Set default min frequency when the screen is off */
	policy->min = policy->cpuinfo.min_freq;
	return NOTIFY_OK;
}

static int msm_drm_notifier_cb(struct notifier_block *nb, unsigned long action,
			  void *data)
{
	struct msm_drm_notifier *evdata = data;
	int *blank = evdata->data;

	/* Parse framebuffer blank events as soon as they occur */
	if (action != MSM_DRM_EARLY_EVENT_BLANK)
		return NOTIFY_OK;

	screen_on = *blank == MSM_DRM_BLANK_UNBLANK;
	return NOTIFY_OK;
}

static int __init freq_limiter_init(void)
{
	int ret;

	cpu_notif.notifier_call = cpu_notifier_cb;
	ret = cpufreq_register_notifier(&cpu_notif, CPUFREQ_POLICY_NOTIFIER);
	if (ret) {
		pr_err("Failed to register cpufreq notifier, err: %d\n", ret);
		goto unregister_cpu_notif;
	}

	msm_drm_notif.notifier_call = msm_drm_notifier_cb;
	msm_drm_notif.priority = INT_MAX;
	ret = msm_drm_register_client(&msm_drm_notif);
	if (ret) {
		pr_err("Failed to register msm_drm notifier, err: %d\n", ret);
		goto unregister_fb_notif;
	}

	return 0;

unregister_fb_notif:
	msm_drm_unregister_client(&msm_drm_notif);
	return ret;
unregister_cpu_notif:
	cpufreq_unregister_notifier(&cpu_notif, CPUFREQ_POLICY_NOTIFIER);
	return ret;
}
subsys_initcall(freq_limiter_init);
