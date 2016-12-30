# Direct Api Examples
These are examples of using the direct api of CQ ( as opposed to the  fluent api)

Contrasted with the fluent api, which is built on the direct api, the base api has these pros and cons

### Pros

  * More explicitly conveys the concepts involved in the code
  * More flexible use of the various objects, for example:
    * Allows direct use of 3D objects, bypassing sketching and 2-D if desired
	
  * Much easier testability, because each object has much less responsibility
  * Operations can be used without Sketches, Workplanes, or even the CQ context

### Cons
  * More verbose
  * easier to make trivial coding mistakes
