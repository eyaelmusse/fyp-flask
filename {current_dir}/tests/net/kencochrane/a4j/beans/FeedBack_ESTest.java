/*
 * This file was automatically generated by EvoSuite
 * Mon Aug 28 01:55:42 GMT 2023
 */

package net.kencochrane.a4j.beans;

import org.junit.Test;
import static org.junit.Assert.*;
import net.kencochrane.a4j.beans.FeedBack;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class FeedBack_ESTest extends FeedBack_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      String string0 = feedBack0.getFeedbackRater();
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      feedBack0.setFeedbackRater("Date = ");
      assertNull(feedBack0.getFeedbackRating());
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      feedBack0.setFeedbackDate((String) null);
      assertNull(feedBack0.getFeedbackDate());
  }

  @Test(timeout = 4000)
  public void test3()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      feedBack0.setFeedbackComments("--------------- \nRater = \nRating = \nComments = null\nDate = null\n--------------- \n");
      assertNull(feedBack0.getFeedbackRating());
  }

  @Test(timeout = 4000)
  public void test4()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      String string0 = feedBack0.getFeedbackDate();
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test5()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      String string0 = feedBack0.getFeedbackRating();
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test6()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      String string0 = feedBack0.getFeedbackComments();
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test7()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      String string0 = feedBack0.toString();
      assertEquals("--------------- \nRater = null\nRating = null\nComments = null\nDate = null\n--------------- \n", string0);
  }

  @Test(timeout = 4000)
  public void test8()  throws Throwable  {
      FeedBack feedBack0 = new FeedBack();
      feedBack0.setFeedbackRating("");
      assertEquals("", feedBack0.getFeedbackRating());
  }
}